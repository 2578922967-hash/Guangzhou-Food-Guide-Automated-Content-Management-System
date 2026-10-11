// 类型定义

export interface Restaurant {
  shop_id: string;
  name: string;
  category: string;
  business_district: string;
  avg_price: number;
  taste_score: number;
  environment_score: number;
  service_score: number;
  star_level: string;
  reviews: number;
  address?: string;
  recommended_dish_1?: string;
  recommended_dish_2?: string;
  recommended_dish_3?: string;
  url?: string;
}

export interface RestaurantFilters {
  name?: string;
  category?: string;
  business_district?: string;
  star_level?: string;
  min_taste_score?: number;
  min_environment_score?: number;
  min_service_score?: number;
  min_rating?: number;
  max_avg_price?: number;
  min_avg_price?: number;
}

export interface Pagination {
  page: number;
  limit: number;
  total: number;
}

export type SortField = "name" | "avg_price" | "taste_score" | "reviews";
export type SortOrder = "asc" | "desc";

