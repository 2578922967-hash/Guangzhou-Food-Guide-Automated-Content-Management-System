// API 客户端

import axios from "axios";
import type { Restaurant, RestaurantFilters } from "../types";

const api = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json",
  },
});

export interface RestaurantListResponse {
  items: Restaurant[];
  count: number;
}

export const restaurantApi = {
  // 获取餐厅列表
  async getRestaurants(
    filters: RestaurantFilters = {},
    limit: number = 20,
    offset: number = 0,
    sortField?: string | null,
    sortOrder: "asc" | "desc" = "desc",
    signal?: AbortSignal
  ): Promise<RestaurantListResponse> {
    const params: Record<string, any> = { 
      limit, 
      offset,
      ...filters 
    };
    
    // 添加排序参数
    if (sortField) {
      params.sort_field = sortField;
      params.sort_order = sortOrder;
    }
    
    // 移除空值
    Object.keys(params).forEach((key) => {
      if (params[key] === undefined || params[key] === null || params[key] === "") {
        delete params[key];
      }
    });
    
    const res = await api.get<RestaurantListResponse>("/restaurants/", { 
      params,
      signal // 支持请求取消
    });
    return res.data;
  },

  // 获取单个餐厅
  async getRestaurant(shopId: string): Promise<Restaurant> {
    const res = await api.get<Restaurant>(`/restaurants/${shopId}`);
    return res.data;
  },

  // 导入CSV
  async importCSV(file: File): Promise<any> {
    const formData = new FormData();
    formData.append("file", file);
    const res = await api.post("/restaurants/import", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return res.data;
  },

  // 健康检查
  async healthCheck(): Promise<{ status: string }> {
    const res = await api.get("/health");
    return res.data;
  },

  // 获取单个餐厅
  async getRestaurant(shopId: string): Promise<Restaurant> {
    const res = await api.get(`/restaurants/${shopId}`);
    return res.data;
  },

  // 更新餐厅
  async updateRestaurant(shopId: string, data: Partial<Restaurant>): Promise<any> {
    const res = await api.put(`/restaurants/${shopId}`, data);
    return res.data;
  },

  // 删除餐厅
  async deleteRestaurant(shopId: string): Promise<any> {
    const res = await api.delete(`/restaurants/${shopId}`);
    return res.data;
  },

  // 批量操作
  async batchOperation(operation: "delete" | "update", shopIds: string[], data?: Partial<Restaurant>): Promise<any> {
    const res = await api.post("/restaurants/batch", {
      operation,
      shop_ids: shopIds,
      data,
    });
    return res.data;
  },

  // 导出 CSV
  async exportCSV(filters: RestaurantFilters = {}): Promise<Blob> {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== "") {
        params.append(key, String(value));
      }
    });
    const queryString = params.toString();
    const url = queryString ? `/restaurants/export/csv?${queryString}` : `/restaurants/export/csv`;
    const res = await api.get(url, {
      responseType: "blob",
    });
    return res.data;
  },

  // 导出 Excel
  async exportExcel(filters: RestaurantFilters = {}): Promise<Blob> {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== "") {
        params.append(key, String(value));
      }
    });
    const queryString = params.toString();
    const url = queryString ? `/restaurants/export/excel?${queryString}` : `/restaurants/export/excel`;
    const res = await api.get(url, {
      responseType: "blob",
    });
    return res.data;
  },
};

