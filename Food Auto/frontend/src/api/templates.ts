// 模板 API 客户端

import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json",
  },
});

export interface Template {
  template_id: number;
  title: string;
  keywords?: string;
  default_format: "text" | "markdown" | "html";
  content: string;
  placeholders_json?: string;
  placeholders?: string[];
  sample_output?: string;
  version?: number;
  updated_at?: string;
}

export interface TemplateListResponse {
  items: Template[];
  count: number;
}

export const templateApi = {
  async listTemplates(): Promise<TemplateListResponse> {
    const res = await api.get<TemplateListResponse>("/templates/");
    return res.data;
  },

  async getTemplate(templateId: number): Promise<Template> {
    const res = await api.get<Template>(`/templates/${templateId}`);
    return res.data;
  },

  async updateTemplate(templateId: number, data: Partial<Template>): Promise<void> {
    await api.put(`/templates/${templateId}`, data);
  },

  async deleteTemplate(templateId: number): Promise<void> {
    await api.delete(`/templates/${templateId}`);
  },
};

