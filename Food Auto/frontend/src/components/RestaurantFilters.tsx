// 筛选组件

import { useState, useEffect, useRef } from "react";
import { useDebounce } from "../utils/useDebounce";
import type { RestaurantFilters } from "../types";

interface RestaurantFiltersProps {
  filters: RestaurantFilters;
  onFiltersChange: (filters: RestaurantFilters) => void;
  categories: string[];
  districts: string[];
  starLevels: string[];
}

export function RestaurantFiltersComponent({
  filters,
  onFiltersChange,
  categories,
  districts,
  starLevels,
}: RestaurantFiltersProps) {
  // 对名称搜索使用防抖，其他筛选条件立即生效
  const [nameInput, setNameInput] = useState(filters.name || "");
  const debouncedName = useDebounce(nameInput, 300); // 300ms 防抖
  const prevDebouncedNameRef = useRef<string>(filters.name || "");
  const isInitialMount = useRef(true);

  // 同步外部 filters.name 到本地 nameInput（仅在外部改变时同步，避免循环更新）
  useEffect(() => {
    const externalName = filters.name || "";
    const currentName = nameInput || "";
    const debouncedNameValue = debouncedName || "";
    
    // 只有当外部名称改变，且与当前输入和防抖值都不同时才同步
    if (externalName !== currentName && externalName !== debouncedNameValue) {
      setNameInput(externalName);
      prevDebouncedNameRef.current = externalName;
    }
  }, [filters.name]); // 只依赖 filters.name

  // 当防抖后的名称改变时，更新筛选条件
  useEffect(() => {
    // 跳过初始挂载时的执行（避免重复触发）
    if (isInitialMount.current) {
      isInitialMount.current = false;
      prevDebouncedNameRef.current = debouncedName;
      return;
    }

    const prevName = prevDebouncedNameRef.current;
    // 只有当防抖后的值与之前的值不同时才更新
    if (debouncedName !== prevName) {
      prevDebouncedNameRef.current = debouncedName;
      // 只有当防抖后的值与当前筛选条件不同时才更新
      const currentFilterName = filters.name || "";
      if (debouncedName !== currentFilterName) {
        const newFilters = { ...filters, name: debouncedName || undefined };
        // 通知父组件
        onFiltersChange(newFilters);
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [debouncedName]); // 只依赖 debouncedName

  const handleChange = (key: keyof RestaurantFilters, value: any) => {
    if (key === "name") {
      // 名称输入直接更新本地状态，防抖会处理 API 请求
      setNameInput(value);
    } else {
      // 其他筛选条件立即生效
      const newFilters = { ...filters, [key]: value || undefined };
      onFiltersChange(newFilters);
    }
  };

  const handleReset = () => {
    const emptyFilters: RestaurantFilters = {};
    setNameInput("");
    onFiltersChange(emptyFilters);
  };

  return (
    <div className="filters-container">
        <h3>Filters</h3>
      <div className="filters-grid">
        <div className="filter-group">
          <label>Search Name</label>
          <input
            type="text"
            placeholder="Enter restaurant name..."
            value={nameInput}
            onChange={(e) => handleChange("name", e.target.value)}
            className="filter-input"
          />
          {nameInput !== debouncedName && (
            <span className="debounce-indicator">Searching...</span>
          )}
        </div>

        <div className="filter-group">
          <label>Cuisine Type</label>
          <select
            value={filters.category || ""}
            onChange={(e) => handleChange("category", e.target.value)}
            className="filter-select"
          >
            <option value="">All</option>
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label>Business District</label>
          <select
            value={filters.business_district || ""}
            onChange={(e) => handleChange("business_district", e.target.value)}
            className="filter-select"
          >
            <option value="">All</option>
            {districts.map((district) => (
              <option key={district} value={district}>
                {district}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label>Star Rating</label>
          <select
            value={filters.star_level || ""}
            onChange={(e) => handleChange("star_level", e.target.value)}
            className="filter-select"
          >
            <option value="">All</option>
            {starLevels.map((level) => (
              <option key={level} value={level}>
                {level}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label>Min Price</label>
          <input
            type="number"
            placeholder="Min price"
            value={filters.min_avg_price || ""}
            onChange={(e) =>
              handleChange("min_avg_price", e.target.value ? Number(e.target.value) : undefined)
            }
            className="filter-input"
            min="0"
          />
        </div>

        <div className="filter-group">
          <label>Max Price</label>
          <input
            type="number"
            placeholder="Max price"
            value={filters.max_avg_price || ""}
            onChange={(e) =>
              handleChange("max_avg_price", e.target.value ? Number(e.target.value) : undefined)
            }
            className="filter-input"
            min="0"
          />
        </div>

        <div className="filter-group">
          <label>Min Taste Score</label>
          <input
            type="number"
            placeholder="Min score"
            value={filters.min_taste_score || ""}
            onChange={(e) =>
              handleChange(
                "min_taste_score",
                e.target.value ? Number(e.target.value) : undefined
              )
            }
            className="filter-input"
            min="0"
            max="10"
            step="0.1"
          />
        </div>

        <div className="filter-group">
          <button onClick={handleReset} className="btn btn-secondary">
            Reset Filters
          </button>
        </div>
      </div>
    </div>
  );
}

