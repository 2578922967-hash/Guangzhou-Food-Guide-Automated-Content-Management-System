// 统计数据 API

import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json",
  },
});

export interface OverallStatistics {
  total_restaurants: number;
  total_categories: number;
  total_districts: number;
  avg_price: number;
  avg_taste_score: number;
  avg_environment_score: number;
  avg_service_score: number;
  total_reviews: number;
  max_price: number;
  min_price: number;
}

export interface CategoryStatistics {
  category: string;
  count: number;
  avg_price: number;
  avg_taste_score: number;
  avg_environment_score: number;
  avg_service_score: number;
}

export interface DistrictStatistics {
  business_district: string;
  count: number;
  avg_price: number;
  avg_taste_score: number;
}

export interface PriceDistribution {
  price_range: string;
  count: number;
}

export interface StarLevelStatistics {
  star_level: string;
  count: number;
  avg_taste_score: number;
  avg_environment_score: number;
  avg_service_score: number;
}

export interface DashboardData {
  overall: OverallStatistics;
  categories: CategoryStatistics[];
  districts: DistrictStatistics[];
  price_distribution: PriceDistribution[];
  star_levels: StarLevelStatistics[];
  top_restaurants: any[];
}

export const statisticsApi = {
  // 获取总体统计
  async getOverallStatistics(): Promise<OverallStatistics> {
    const res = await api.get("/statistics/overall");
    return res.data;
  },

  // 获取菜系统计
  async getCategoryStatistics(): Promise<CategoryStatistics[]> {
    const res = await api.get("/statistics/categories");
    return res.data;
  },

  // 获取商圈统计
  async getDistrictStatistics(): Promise<DistrictStatistics[]> {
    const res = await api.get("/statistics/districts");
    return res.data;
  },

  // 获取价格分布
  async getPriceDistribution(): Promise<PriceDistribution[]> {
    const res = await api.get("/statistics/price-distribution");
    return res.data;
  },

  // 获取星级统计
  async getStarLevelStatistics(): Promise<StarLevelStatistics[]> {
    const res = await api.get("/statistics/star-levels");
    return res.data;
  },

  // 获取热门餐厅
  async getTopRestaurants(limit: number = 10, orderBy: string = "taste_score", orderDirection: string = "DESC"): Promise<any[]> {
    const res = await api.get("/statistics/top-restaurants", {
      params: { limit, order_by: orderBy, order_direction: orderDirection },
    });
    return res.data;
  },

  // 获取仪表板数据
  async getDashboardData(): Promise<DashboardData> {
    const res = await api.get("/statistics/dashboard");
    return res.data;
  },
};

