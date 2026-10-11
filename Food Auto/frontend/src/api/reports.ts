// 报告 API 客户端

import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json",
  },
});

export interface ReportGenerateRequest {
  template_id: number;
  params?: Record<string, any>;
  format?: "text" | "markdown" | "html";
  save?: boolean;
}

export interface ReportGenerateResponse {
  title: string;
  keywords?: string;
  format: "text" | "markdown" | "html";
  text: string;
  markdown: string;
  html: string;
  selected_format?: string;
  selected_content?: string;
  context?: Record<string, any>;
  report_id?: number;
  output_path?: string;
}

export const reportApi = {
  async generateReport(request: ReportGenerateRequest): Promise<ReportGenerateResponse> {
    const res = await api.post<ReportGenerateResponse>("/reports/generate", request);
    return res.data;
  },
};

