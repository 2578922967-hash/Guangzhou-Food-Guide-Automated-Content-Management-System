// 餐厅数据 Hook

import { useState, useEffect, useCallback, useRef, useMemo } from "react";
import { restaurantApi } from "../api/restaurants";
import type { Restaurant, RestaurantFilters, SortField, SortOrder } from "../types";

interface UseRestaurantsOptions {
  initialFilters?: RestaurantFilters;
  initialLimit?: number;
  initialPage?: number;
}

export function useRestaurants(options: UseRestaurantsOptions = {}) {
  const { initialFilters = {}, initialLimit = 20, initialPage = 1 } = options;

  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<RestaurantFilters>(initialFilters);
  const [limit, setLimit] = useState(initialLimit);
  const [page, setPage] = useState(initialPage);
  const [total, setTotal] = useState(0);
  const [sortField, setSortField] = useState<SortField | null>(null);
  const [sortOrder, setSortOrder] = useState<SortOrder>("desc");
  
  // 请求取消标识
  const abortControllerRef = useRef<AbortController | null>(null);
  // 请求缓存（简单的内存缓存）
  const cacheRef = useRef<Map<string, { data: Restaurant[]; count: number; timestamp: number }>>(
    new Map()
  );
  const CACHE_TTL = 30000; // 30秒缓存

  // 生成缓存键
  const getCacheKey = useCallback((f: RestaurantFilters, l: number, p: number, s?: SortField | null, o?: SortOrder) => {
    return JSON.stringify({ filters: f, limit: l, page: p, sortField: s, sortOrder: o });
  }, []);

  // 检查缓存是否有效
  const getCachedData = useCallback((key: string) => {
    const cached = cacheRef.current.get(key);
    if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
      return cached;
    }
    if (cached) {
      cacheRef.current.delete(key); // 删除过期缓存
    }
    return null;
  }, []);

  const fetchRestaurants = useCallback(async () => {
    // 取消之前的请求
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    abortControllerRef.current = new AbortController();

    const cacheKey = getCacheKey(filters, limit, page, sortField, sortOrder);
    const cached = getCachedData(cacheKey);
    
    if (cached) {
      setRestaurants(cached.data);
      setTotal(cached.count);
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);
    try {
      // 计算 offset
      const offset = (page - 1) * limit;
      // 获取数据：使用 limit 而不是获取所有数据，并传递取消信号
      const response = await restaurantApi.getRestaurants(
        filters, 
        limit, 
        offset, 
        sortField, 
        sortOrder,
        abortControllerRef.current.signal
      );
      
      // 缓存结果
      cacheRef.current.set(cacheKey, {
        data: response.items,
        count: response.count,
        timestamp: Date.now(),
      });

      setRestaurants(response.items);
      setTotal(response.count);
    } catch (err: any) {
      // 忽略取消的请求
      if (err.name === "AbortError" || err.message === "canceled") {
        return;
      }
      console.error("获取餐厅数据失败:", err);
      setError(err.response?.data?.error || err.message || "获取数据失败");
      setRestaurants([]);
      setTotal(0);
    } finally {
      setLoading(false);
    }
  }, [filters, limit, page, sortField, sortOrder, getCacheKey, getCachedData]);

  useEffect(() => {
    fetchRestaurants();
    return () => {
      // 组件卸载时取消请求
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, [fetchRestaurants]);

  const updateFilters = useCallback((newFilters: RestaurantFilters) => {
    setFilters(newFilters);
    setPage(1); // 重置到第一页
    // 清除相关缓存
    cacheRef.current.clear();
  }, []);

  const updateLimit = useCallback((newLimit: number) => {
    setLimit(newLimit);
    setPage(1); // 重置到第一页
    cacheRef.current.clear();
  }, []);

  const updatePage = useCallback((newPage: number) => {
    setPage(newPage);
  }, []);

  const handleSort = useCallback((field: SortField, order: SortOrder) => {
    setSortField(field);
    setSortOrder(order);
    setPage(1); // 重置到第一页
    cacheRef.current.clear();
  }, []);

  // 获取所有分类和商圈（用于筛选下拉框）- 只加载一次并缓存
  const [categories, setCategories] = useState<string[]>([]);
  const [districts, setDistricts] = useState<string[]>([]);
  const [starLevels, setStarLevels] = useState<string[]>([]);
  const optionsLoadedRef = useRef(false);

  useEffect(() => {
    // 只在首次加载时获取选项
    if (optionsLoadedRef.current) return;
    
    const fetchOptions = async () => {
      try {
        // 使用较大的 limit 获取选项（只需要去重），offset=0
        const response = await restaurantApi.getRestaurants({}, 1000, 0);
        const cats = [...new Set(response.items.map((r) => r.category).filter(Boolean))].sort();
        const dists = [
          ...new Set(response.items.map((r) => r.business_district).filter(Boolean)),
        ].sort();
        const stars = [...new Set(response.items.map((r) => r.star_level).filter(Boolean))].sort();
        setCategories(cats);
        setDistricts(dists);
        setStarLevels(stars);
        optionsLoadedRef.current = true;
      } catch (err) {
        console.error("获取选项数据失败:", err);
        // 即使失败也标记为已加载，避免重复请求
        optionsLoadedRef.current = true;
      }
    };
    fetchOptions();
  }, []);

  // 计算总页数
  const totalPages = useMemo(() => Math.ceil(total / limit), [total, limit]);

  return {
    restaurants,
    loading,
    error,
    filters,
    limit,
    page,
    total,
    totalPages,
    categories,
    districts,
    starLevels,
    updateFilters,
    updateLimit,
    updatePage,
    handleSort,
    refetch: fetchRestaurants,
  };
}

