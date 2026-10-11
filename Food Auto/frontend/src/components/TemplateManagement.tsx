// 模板管理组件

import { useState, useEffect } from "react";
import { templateApi, type Template } from "../api/templates";
import { LoadingSpinner } from "./LoadingSpinner";

export function TemplateManagement() {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState<Partial<Template>>({});

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await templateApi.listTemplates();
      setTemplates(response.items);
    } catch (err: any) {
      setError(err.message || "Failed to load templates");
    } finally {
      setLoading(false);
    }
  };

  const handleSelectTemplate = async (templateId: number) => {
    try {
      const template = await templateApi.getTemplate(templateId);
      setSelectedTemplate(template);
      setFormData(template);
      setEditing(false);
    } catch (err: any) {
      alert("Failed to load template: " + (err.message || "Unknown error"));
    }
  };

  const handleSave = async () => {
    if (!selectedTemplate) return;

    try {
      await templateApi.updateTemplate(selectedTemplate.template_id, formData);
      alert("Saved successfully");
      setEditing(false);
      await fetchTemplates();
      if (selectedTemplate) {
        const updated = await templateApi.getTemplate(selectedTemplate.template_id);
        setSelectedTemplate(updated);
        setFormData(updated);
      }
    } catch (err: any) {
      alert("Save failed: " + (err.message || "Unknown error"));
    }
  };

  const handleCancel = () => {
    if (selectedTemplate) {
      setFormData(selectedTemplate);
    }
    setEditing(false);
  };

  if (loading) {
    return (
      <div className="loading-container">
        <LoadingSpinner size="large" text="Loading templates..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-banner">
        <p className="error">{error}</p>
      </div>
    );
  }

  return (
    <div className="template-management">
      <div className="template-list-section">
        <h2>Template List</h2>
        <div className="template-list">
          {templates.map((template) => (
            <div
              key={template.template_id}
              className={`template-card ${selectedTemplate?.template_id === template.template_id ? "selected" : ""}`}
              onClick={() => handleSelectTemplate(template.template_id)}
            >
              <h3>{template.title}</h3>
              <p className="template-keywords">{template.keywords || "No keywords"}</p>
              <p className="template-format">Format: {template.default_format}</p>
              <p className="template-id">ID: {template.template_id}</p>
            </div>
          ))}
        </div>
      </div>

      {selectedTemplate && (
        <div className="template-detail-section">
          <div className="template-detail-header">
            <h2>Template Details</h2>
            <div style={{ display: "flex", gap: "0.5rem" }}>
              {!editing && (
                <button className="btn btn-primary" onClick={() => setEditing(true)}>
                  Edit
                </button>
              )}
            </div>
          </div>

          {editing ? (
            <div className="template-form">
              <div className="form-group">
                <label>Title</label>
                <input
                  type="text"
                  value={formData.title || ""}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label>Keywords</label>
                <input
                  type="text"
                  value={formData.keywords || ""}
                  onChange={(e) => setFormData({ ...formData, keywords: e.target.value })}
                  className="form-input"
                  placeholder="Separated by commas"
                />
              </div>

              <div className="form-group">
                <label>Default Format</label>
                <select
                  value={formData.default_format || "text"}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      default_format: e.target.value as "text" | "markdown" | "html",
                    })
                  }
                  className="form-input"
                >
                  <option value="text">Text</option>
                  <option value="markdown">Markdown</option>
                  <option value="html">HTML</option>
                </select>
              </div>

              <div className="form-group">
                <label>Content</label>
                <textarea
                  value={formData.content || ""}
                  onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                  className="form-textarea"
                  rows={20}
                />
              </div>

              <div className="form-group">
                <label>Placeholders (JSON)</label>
                <textarea
                  value={formData.placeholders_json || ""}
                  onChange={(e) =>
                    setFormData({ ...formData, placeholders_json: e.target.value })
                  }
                  className="form-textarea"
                  rows={5}
                  placeholder='Example: ["{name}", "{price}"]'
                />
              </div>

              <div className="form-group">
                <label>Sample Output</label>
                <textarea
                  value={formData.sample_output || ""}
                  onChange={(e) => setFormData({ ...formData, sample_output: e.target.value })}
                  className="form-textarea"
                  rows={10}
                />
              </div>

              <div className="form-actions">
                <button className="btn btn-primary" onClick={handleSave}>
                  Save
                </button>
                <button className="btn btn-secondary" onClick={handleCancel}>
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <div className="template-detail">
              <div className="detail-row">
                <span className="detail-label">Template ID:</span>
                <span className="detail-value">{selectedTemplate.template_id}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Title:</span>
                <span className="detail-value">{selectedTemplate.title}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Keywords:</span>
                <span className="detail-value">{selectedTemplate.keywords || "-"}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Default Format:</span>
                <span className="detail-value">{selectedTemplate.default_format}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Placeholders:</span>
                <span className="detail-value">
                  {selectedTemplate.placeholders && Array.isArray(selectedTemplate.placeholders) && selectedTemplate.placeholders.length > 0
                    ? selectedTemplate.placeholders.map((p: string) => `{${p}}`).join(", ")
                    : "-"}
                </span>
              </div>
              <div className="detail-row-full">
                <span className="detail-label">Content:</span>
                <pre className="template-content">{selectedTemplate.content}</pre>
              </div>
              {selectedTemplate.sample_output && (
                <div className="detail-row-full">
                  <span className="detail-label">Sample Output:</span>
                  <pre className="template-sample">{selectedTemplate.sample_output}</pre>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

