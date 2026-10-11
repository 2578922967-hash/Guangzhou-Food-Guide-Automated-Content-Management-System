// 餐厅表格组件

import { useState, useMemo } from "react";
import type { Restaurant, SortField, SortOrder } from "../types";
import { LoadingSpinner, SkeletonTable } from "./LoadingSpinner";
import { StarRating } from "./StarRating";

interface RestaurantTableProps {
  restaurants: Restaurant[];
  loading?: boolean;
  onSort?: (field: SortField, order: SortOrder) => void;
  onSelect?: (shopIds: string[]) => void;
  onRowClick?: (restaurant: Restaurant) => void;
  selectedIds?: string[];
}

export function RestaurantTable({
  restaurants,
  loading = false,
  onSort,
  onSelect,
  onRowClick,
  selectedIds = [],
}: RestaurantTableProps) {
  const [sortField, setSortField] = useState<SortField | null>(null);
  const [sortOrder, setSortOrder] = useState<SortOrder>("desc");

  const handleSelectAll = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (onSelect) {
      const currentPageIds = restaurants.map(r => r.shop_id);
      if (e.target.checked) {
        // 添加当前页面的所有餐厅（避免重复）
        const newSelectedIds = [...new Set([...selectedIds, ...currentPageIds])];
        onSelect(newSelectedIds);
      } else {
        // 只取消选择当前页面的餐厅
        onSelect(selectedIds.filter(id => !currentPageIds.includes(id)));
      }
    }
  };

  const handleSelectOne = (shopId: string, checked: boolean) => {
    if (onSelect) {
      if (checked) {
        // 避免重复添加
        if (!selectedIds.includes(shopId)) {
          onSelect([...selectedIds, shopId]);
        }
      } else {
        onSelect(selectedIds.filter(id => id !== shopId));
      }
    }
  };

  // 检查当前页面的所有餐厅是否都被选中
  const currentPageIds = restaurants.map(r => r.shop_id);
  const allSelected = restaurants.length > 0 && currentPageIds.every(id => selectedIds.includes(id));
  const someSelected = currentPageIds.some(id => selectedIds.includes(id)) && !allSelected;

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      const newOrder = sortOrder === "asc" ? "desc" : "asc";
      setSortOrder(newOrder);
      onSort?.(field, newOrder);
    } else {
      setSortField(field);
      setSortOrder("desc");
      onSort?.(field, "desc");
    }
  };

  const SortIcon = ({ field }: { field: SortField }) => {
    if (sortField !== field) return <span className="sort-icon">↕</span>;
    return <span className="sort-icon">{sortOrder === "asc" ? "↑" : "↓"}</span>;
  };

  if (loading) {
    return (
      <div className="table-container">
        <SkeletonTable />
      </div>
    );
  }

  if (restaurants.length === 0) {
    return (
      <div className="empty-container">
        <p>No restaurant data available</p>
      </div>
    );
  }

  return (
    <div className="table-container">
      <table className="restaurant-table">
        <thead>
          <tr>
            {onSelect && (
              <th className="select-column">
                <input
                  type="checkbox"
                  checked={allSelected}
                  ref={(input) => {
                    if (input) input.indeterminate = someSelected;
                  }}
                  onChange={handleSelectAll}
                  onClick={(e) => e.stopPropagation()}
                />
              </th>
            )}
            <th onClick={() => handleSort("name")} className="sortable">
              Name <SortIcon field="name" />
            </th>
            <th>Cuisine Type</th>
            <th>Business District</th>
            <th onClick={() => handleSort("avg_price")} className="sortable">
              Avg. Price <SortIcon field="avg_price" />
            </th>
            <th onClick={() => handleSort("taste_score")} className="sortable">
              Taste Score <SortIcon field="taste_score" />
            </th>
            <th>Environment Score</th>
            <th>Service Score</th>
            <th>Star Rating</th>
            <th onClick={() => handleSort("reviews")} className="sortable">
              Reviews <SortIcon field="reviews" />
            </th>
            {onRowClick && <th style={{ width: "100px" }}>Actions</th>}
          </tr>
        </thead>
        <tbody>
          {restaurants.map((item) => {
            const isSelected = selectedIds.includes(item.shop_id);
            return (
              <tr
                key={item.shop_id}
                className={isSelected ? "selected" : ""}
                style={{ cursor: onRowClick ? "pointer" : "default" }}
              >
                {onSelect && (
                  <td className="select-column" onClick={(e) => e.stopPropagation()}>
                    <input
                      type="checkbox"
                      checked={isSelected}
                      onChange={(e) => handleSelectOne(item.shop_id, e.target.checked)}
                      onClick={(e) => e.stopPropagation()}
                    />
                  </td>
                )}
                <td
                  className="name-cell"
                  onClick={() => onRowClick?.(item)}
                  style={{ cursor: onRowClick ? "pointer" : "default" }}
                >
                  {item.name}
                </td>
                <td>{item.category}</td>
                <td>{item.business_district || "-"}</td>
                <td className="price-cell">
                  {item.avg_price ? `¥${item.avg_price}` : "-"}
                </td>
                <td className="score-cell">{item.taste_score?.toFixed(1) ?? "-"}</td>
                <td className="score-cell">
                  {item.environment_score?.toFixed(1) ?? "-"}
                </td>
                <td className="score-cell">
                  {item.service_score?.toFixed(1) ?? "-"}
                </td>
                <td>
                  <StarRating starLevel={item.star_level} size="small" />
                </td>
                <td>{item.reviews ?? 0}</td>
                {onRowClick && (
                  <td onClick={(e) => e.stopPropagation()}>
                    <button
                      className="btn btn-sm btn-primary"
                      onClick={(e) => {
                        e.stopPropagation();
                        onRowClick(item);
                      }}
                    >
                      View Details
                    </button>
                  </td>
                )}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

