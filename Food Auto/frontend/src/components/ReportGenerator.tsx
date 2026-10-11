// 报告生成组件

import { useState, useEffect, useRef } from "react";
import { templateApi, type Template } from "../api/templates";
import { reportApi, type ReportGenerateRequest, type ReportGenerateResponse } from "../api/reports";
import { restaurantApi } from "../api/restaurants";

export function ReportGenerator() {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [selectedTemplateId, setSelectedTemplateId] = useState<number | null>(null);
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);
  const [params, setParams] = useState<Record<string, any>>({});
  const [format, setFormat] = useState<"text" | "markdown" | "html">("text");
  const [save, setSave] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [report, setReport] = useState<ReportGenerateResponse | null>(null);
  const [districts, setDistricts] = useState<string[]>([]);
  const chartInitializedRef = useRef(false);

  useEffect(() => {
    const initialize = async () => {
      await fetchTemplates();
      await fetchDistricts();
    };
    initialize();
  }, []);

  useEffect(() => {
    if (selectedTemplateId) {
      // 如果模板需要 district，等待 districts 加载完成
      const needsDistrict = [4, 5, 6].includes(selectedTemplateId);
      if (!needsDistrict || districts.length > 0) {
        loadTemplate(selectedTemplateId);
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedTemplateId, districts]);

  const fetchTemplates = async () => {
    try {
      const response = await templateApi.listTemplates();
      setTemplates(response.items);
      if (response.items.length > 0 && !selectedTemplateId) {
        setSelectedTemplateId(response.items[0].template_id);
      }
    } catch (err: any) {
      setError(err.message || "Failed to load templates");
    }
  };

  const fetchDistricts = async () => {
    try {
      const response = await restaurantApi.getRestaurants({}, 1000, 0);
      const dists = [
        ...new Set(response.items.map((r) => r.business_district).filter(Boolean)),
      ].sort();
      setDistricts(dists);
    } catch (err) {
      console.error("Failed to fetch districts:", err);
    }
  };

  const loadTemplate = async (templateId: number) => {
    try {
      const template = await templateApi.getTemplate(templateId);
      setSelectedTemplate(template);
      setFormat(template.default_format);
      // 根据模板 ID 初始化参数
      initializeParams(templateId, template);
    } catch (err: any) {
      setError(err.message || "Failed to load templates");
    }
  };

  const initializeParams = (templateId: number, template: Template) => {
    const newParams: Record<string, any> = {};
    
    // 根据模板 ID 设置默认参数
    switch (templateId) {
      case 2: // Best Value for Money
        newParams.price_cap = 80;
        newParams.top_n = 5;
        break;
      case 4: // Hidden Gems
      case 5: // District Food Express
      case 6: // Top Delivery Picks
        if (districts.length > 0) {
          newParams.district = districts[0];
        }
        if (templateId === 6) {
          newParams.min_score = 8.5;
        }
        break;
      // Template 7 (Statistics Visualization) doesn't need parameters
    }
    
    setParams(newParams);
  };

  const handleGenerate = async () => {
    if (!selectedTemplateId) {
      // 使用Toast通知，需要在父组件中传入
      alert("Please select a template");
      return;
    }

    // 验证必需参数
    const needsDistrict = [4, 5, 6].includes(selectedTemplateId);
    if (needsDistrict && !params.district) {
      alert("Please select a business district");
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setReport(null);

      const request: ReportGenerateRequest = {
        template_id: selectedTemplateId,
        params,
        format,
        save,
      };

      const result = await reportApi.generateReport(request);
      setReport(result);
      // 重置图表初始化标志，以便在HTML渲染后重新初始化
      if (selectedTemplateId === 7) {
        chartInitializedRef.current = false;
      }
      // 生成报告后，滚动到报告输出区域
      setTimeout(() => {
        const reportOutput = document.querySelector(".report-output");
        if (reportOutput) {
          reportOutput.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      }, 100);
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || err.message || "Failed to generate report";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    // Toast通知将在父组件中显示
  };

  const handleDownload = (content: string, filename: string) => {
    const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
  };

// HTML报告内容组件，用于处理图表初始化
function HtmlReportContent({
  html,
  context,
  templateId,
  onInitialized,
}: {
  html: string;
  context?: Record<string, any>;
  templateId: number | null;
  onInitialized: () => void;
}) {
  const containerRef = useRef<HTMLDivElement>(null);
  const chartsInitializedRef = useRef(false);

  useEffect(() => {
    // 当切换格式或模板时，重置初始化标志
    chartsInitializedRef.current = false;
  }, [html, templateId]);

  useEffect(() => {
    if (templateId === 7 && context && containerRef.current && !chartsInitializedRef.current) {
      chartsInitializedRef.current = true;
      // 延迟执行，确保HTML已经渲染
      setTimeout(() => {
        if (containerRef.current) {
          initializeCharts(containerRef.current, context);
          onInitialized();
        }
      }, 200);
    }
  }, [html, context, templateId, onInitialized]);

  return (
    <div
      className="report-html"
      ref={containerRef}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

  const initializeCharts = (container: HTMLElement, context: any) => {
    // 动态加载Chart.js
    if ((window as any).Chart) {
      renderCharts(container, context);
    } else {
      const script = document.createElement("script");
      script.src = "https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js";
      script.onload = () => renderCharts(container, context);
      document.head.appendChild(script);
    }
  };

  const renderCharts = (container: HTMLElement, context: any) => {
    const Chart = (window as any).Chart;
    if (!Chart) return;

    // 解析JSON数据
    const categoryLabels = typeof context.category_labels_json === 'string' 
      ? JSON.parse(context.category_labels_json) 
      : context.category_labels_json || [];
    const categoryCounts = typeof context.category_counts_json === 'string'
      ? JSON.parse(context.category_counts_json)
      : context.category_counts_json || [];
    
    const districtLabels = typeof context.district_labels_json === 'string'
      ? JSON.parse(context.district_labels_json)
      : context.district_labels_json || [];
    const districtCounts = typeof context.district_counts_json === 'string'
      ? JSON.parse(context.district_counts_json)
      : context.district_counts_json || [];
    
    const priceLabels = typeof context.price_labels_json === 'string'
      ? JSON.parse(context.price_labels_json)
      : context.price_labels_json || [];
    const priceCounts = typeof context.price_counts_json === 'string'
      ? JSON.parse(context.price_counts_json)
      : context.price_counts_json || [];
    
    const starLabels = typeof context.star_labels_json === 'string'
      ? JSON.parse(context.star_labels_json)
      : context.star_labels_json || [];
    const starCounts = typeof context.star_counts_json === 'string'
      ? JSON.parse(context.star_counts_json)
      : context.star_counts_json || [];

    // 初始化Category Chart
    const categoryCanvas = container.querySelector("#categoryChart") as HTMLCanvasElement;
    if (categoryCanvas && categoryLabels.length > 0) {
      const categoryCtx = categoryCanvas.getContext("2d");
      if (categoryCtx) {
        // 清理已存在的图表实例
        const existingChart = (categoryCanvas as any).chartInstance;
        if (existingChart && typeof existingChart.destroy === 'function') {
          existingChart.destroy();
        }
        
        const chart = new Chart(categoryCtx, {
          type: "bar",
          data: {
            labels: categoryLabels,
            datasets: [{
              label: "Number of Restaurants",
              data: categoryCounts,
              backgroundColor: "rgba(54, 162, 235, 0.6)",
              borderColor: "rgba(54, 162, 235, 1)",
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: true
              }
            },
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      }
    }

    // 初始化District Chart
    const districtCanvas = container.querySelector("#districtChart") as HTMLCanvasElement;
    if (districtCanvas && districtLabels.length > 0) {
      const districtCtx = districtCanvas.getContext("2d");
      if (districtCtx) {
        // 清理已存在的图表实例
        const existingChart = (districtCanvas as any).chartInstance;
        if (existingChart && typeof existingChart.destroy === 'function') {
          existingChart.destroy();
        }
        
        const chart = new Chart(districtCtx, {
          type: "pie",
          data: {
            labels: districtLabels,
            datasets: [{
              data: districtCounts,
              backgroundColor: [
                "rgba(255, 99, 132, 0.6)",
                "rgba(54, 162, 235, 0.6)",
                "rgba(255, 206, 86, 0.6)",
                "rgba(75, 192, 192, 0.6)",
                "rgba(153, 102, 255, 0.6)",
                "rgba(255, 159, 64, 0.6)",
                "rgba(199, 199, 199, 0.6)",
                "rgba(83, 102, 255, 0.6)",
                "rgba(255, 99, 255, 0.6)",
                "rgba(99, 255, 132, 0.6)"
              ]
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false
          }
        });
        (districtCanvas as any).chartInstance = chart;
      }
    }

    // 初始化Price Chart
    const priceCanvas = container.querySelector("#priceChart") as HTMLCanvasElement;
    if (priceCanvas && priceLabels.length > 0) {
      const priceCtx = priceCanvas.getContext("2d");
      if (priceCtx) {
        // 清理已存在的图表实例
        const existingChart = (priceCanvas as any).chartInstance;
        if (existingChart && typeof existingChart.destroy === 'function') {
          existingChart.destroy();
        }
        
        const chart = new Chart(priceCtx, {
          type: "line",
          data: {
            labels: priceLabels,
            datasets: [{
              label: "Number of Restaurants",
              data: priceCounts,
              borderColor: "rgba(75, 192, 192, 1)",
              backgroundColor: "rgba(75, 192, 192, 0.2)",
              tension: 0.1
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: true
              }
            },
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
        (priceCanvas as any).chartInstance = chart;
      }
    }

    // 初始化Star Chart
    const starCanvas = container.querySelector("#starChart") as HTMLCanvasElement;
    if (starCanvas && starLabels.length > 0) {
      const starCtx = starCanvas.getContext("2d");
      if (starCtx) {
        // 清理已存在的图表实例
        const existingChart = (starCanvas as any).chartInstance;
        if (existingChart && typeof existingChart.destroy === 'function') {
          existingChart.destroy();
        }
        
        const chart = new Chart(starCtx, {
          type: "doughnut",
          data: {
            labels: starLabels,
            datasets: [{
              data: starCounts,
              backgroundColor: [
                "rgba(255, 215, 0, 0.6)",
                "rgba(192, 192, 192, 0.6)",
                "rgba(205, 127, 50, 0.6)",
                "rgba(255, 99, 132, 0.6)",
                "rgba(54, 162, 235, 0.6)"
              ]
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false
          }
        });
        (starCanvas as any).chartInstance = chart;
      }
    }
  };

  return (
    <div className="report-generator">
      <div className="report-config">
        <h2>Report Generator</h2>

        <div className="config-section">
          <label>Select Template</label>
          <select
            value={selectedTemplateId || ""}
            onChange={(e) => setSelectedTemplateId(Number(e.target.value))}
            className="form-select"
          >
            <option value="">Please select a template</option>
            {templates.map((template) => (
              <option key={template.template_id} value={template.template_id}>
                {template.title} (ID: {template.template_id})
              </option>
            ))}
          </select>
        </div>

        {selectedTemplate && (
          <>
            <div className="config-section">
              <label>Template Information</label>
              <div className="template-info">
                <p>
                  <strong>Title:</strong> {selectedTemplate.title}
                </p>
                <p>
                  <strong>Format:</strong> {selectedTemplate.default_format}
                </p>
                {selectedTemplate.keywords && (
                  <p>
                    <strong>Keywords:</strong> {selectedTemplate.keywords}
                  </p>
                )}
              </div>
            </div>

            <div className="config-section">
              <label>Parameters</label>
              <div className="params-form">
                {selectedTemplateId === 2 && (
                  <>
                    <div className="param-group">
                      <label>Price Cap (¥)</label>
                      <input
                        type="number"
                        value={params.price_cap || 80}
                        onChange={(e) =>
                          setParams({ ...params, price_cap: Number(e.target.value) })
                        }
                        className="form-input"
                      />
                    </div>
                    <div className="param-group">
                      <label>Number of Recommendations</label>
                      <input
                        type="number"
                        value={params.top_n || 5}
                        onChange={(e) => setParams({ ...params, top_n: Number(e.target.value) })}
                        className="form-input"
                      />
                    </div>
                  </>
                )}

                {(selectedTemplateId === 4 ||
                  selectedTemplateId === 5 ||
                  selectedTemplateId === 6) && (
                  <div className="param-group">
                    <label>Business District</label>
                    <select
                      value={params.district || ""}
                      onChange={(e) => setParams({ ...params, district: e.target.value })}
                      className="form-select"
                    >
                      <option value="">Please select a business district</option>
                      {districts.map((district) => (
                        <option key={district} value={district}>
                          {district}
                        </option>
                      ))}
                    </select>
                  </div>
                )}

                {selectedTemplateId === 6 && (
                  <div className="param-group">
                    <label>Minimum Score</label>
                    <input
                      type="number"
                      step="0.1"
                      min="0"
                      max="10"
                      value={params.min_score || 8.5}
                      onChange={(e) =>
                        setParams({ ...params, min_score: Number(e.target.value) })
                      }
                      className="form-input"
                    />
                  </div>
                )}
              </div>
            </div>

            <div className="config-section">
              <label>Output Format</label>
              <select
                value={format}
                onChange={(e) => setFormat(e.target.value as "text" | "markdown" | "html")}
                className="form-select"
              >
                <option value="text">Text</option>
                <option value="markdown">Markdown</option>
                <option value="html">HTML</option>
              </select>
            </div>

            <div className="config-section">
              <label>
                <input
                  type="checkbox"
                  checked={save}
                  onChange={(e) => setSave(e.target.checked)}
                />
                Save report to database
              </label>
            </div>

            <div className="config-actions">
              <button
                className="btn btn-primary"
                onClick={handleGenerate}
                disabled={loading}
              >
                {loading ? "Generating..." : "Generate Report"}
              </button>
            </div>
          </>
        )}
      </div>

      {error && (
        <div className="error-banner">
          <p className="error">{error}</p>
        </div>
      )}

      {report && (
        <div className="report-output">
          <div className="report-header">
            <h2>{report.title}</h2>
            <div className="report-actions">
              <button
                className="btn btn-secondary btn-sm"
                onClick={() => {
                  const content =
                    format === "html"
                      ? report.html
                      : format === "markdown"
                      ? report.markdown
                      : report.text;
                  handleCopy(content);
                }}
              >
                Copy
              </button>
              <button
                className="btn btn-secondary btn-sm"
                onClick={() => {
                  const content =
                    format === "html"
                      ? report.html
                      : format === "markdown"
                      ? report.markdown
                      : report.text;
                  const ext = format === "html" ? "html" : format === "markdown" ? "md" : "txt";
                  handleDownload(content, `${report.title}.${ext}`);
                }}
              >
                Download
              </button>
            </div>
          </div>

          <div className="report-content">
            {format === "html" ? (
              <HtmlReportContent
                html={report.html}
                context={report.context}
                templateId={selectedTemplateId}
                onInitialized={() => {
                  chartInitializedRef.current = true;
                }}
              />
            ) : format === "markdown" ? (
              <pre className="report-text">{report.markdown}</pre>
            ) : (
              <pre className="report-text">{report.text}</pre>
            )}
          </div>

            <div className="report-formats">
              <h3>Switch Format</h3>
              <div className="format-tabs">
                <button
                  className={`format-tab ${format === "text" ? "active" : ""}`}
                  onClick={() => setFormat("text")}
                >
                  Text
                </button>
                <button
                  className={`format-tab ${format === "markdown" ? "active" : ""}`}
                  onClick={() => setFormat("markdown")}
                >
                  Markdown
                </button>
                <button
                  className={`format-tab ${format === "html" ? "active" : ""}`}
                  onClick={() => setFormat("html")}
                >
                  HTML
                </button>
              </div>
            </div>
        </div>
      )}
    </div>
  );
}

