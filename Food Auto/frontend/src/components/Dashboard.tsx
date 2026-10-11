// 统计仪表板组件

import { useState, useEffect } from "react";
import { statisticsApi } from "../api/statistics";
import type { DashboardData } from "../api/statistics";
import { LoadingSpinner } from "./LoadingSpinner";
import { StarRating } from "./StarRating";

export function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const dashboardData = await statisticsApi.getDashboardData();
        setData(dashboardData);
      } catch (err: any) {
        setError(err.message || "Failed to load data");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="dashboard-container">
        <LoadingSpinner size="large" text="Loading data..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-container">
        <div className="error-banner">
          <p className="error">{error}</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return null;
  }

  const { overall, categories, districts, price_distribution, star_levels, top_restaurants } = data;

  return (
    <div className="dashboard-container">
      <header>
        <h1>Statistics Dashboard</h1>
        <p>Guangzhou Food Data Statistics and Analysis</p>
      </header>

      {/* 总体统计 */}
      <section className="stats-section">
        <h2>Overall Statistics</h2>
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-label">Total Restaurants</div>
            <div className="stat-value">{overall.total_restaurants || 0}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Cuisine Types</div>
            <div className="stat-value">{overall.total_categories || 0}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Business Districts</div>
            <div className="stat-value">{overall.total_districts || 0}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Average Price</div>
            <div className="stat-value">¥{overall.avg_price?.toFixed(0) || 0}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Avg. Taste Score</div>
            <div className="stat-value">{overall.avg_taste_score?.toFixed(1) || 0}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Avg. Environment Score</div>
            <div className="stat-value">{overall.avg_environment_score?.toFixed(1) || 0}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Avg. Service Score</div>
            <div className="stat-value">{overall.avg_service_score?.toFixed(1) || 0}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Total Reviews</div>
            <div className="stat-value">{overall.total_reviews || 0}</div>
          </div>
        </div>
      </section>

      {/* 菜系统计 */}
      <section className="stats-section">
        <h2>Cuisine Distribution (Top 10)</h2>
        <div className="table-container">
          <table className="stats-table">
            <thead>
              <tr>
                <th>Cuisine Type</th>
                <th>Count</th>
                <th>Avg. Price</th>
                <th>Avg. Taste Score</th>
                <th>Avg. Environment Score</th>
                <th>Avg. Service Score</th>
              </tr>
            </thead>
            <tbody>
              {categories.slice(0, 10).map((cat) => (
                <tr key={cat.category}>
                  <td>{cat.category}</td>
                  <td>{cat.count}</td>
                  <td>¥{cat.avg_price?.toFixed(0) || 0}</td>
                  <td>{cat.avg_taste_score?.toFixed(1) || 0}</td>
                  <td>{cat.avg_environment_score?.toFixed(1) || 0}</td>
                  <td>{cat.avg_service_score?.toFixed(1) || 0}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* 商圈统计 */}
      <section className="stats-section">
        <h2>Business District Distribution (Top 10)</h2>
        <div className="table-container">
          <table className="stats-table">
            <thead>
              <tr>
                <th>Business District</th>
                <th>Count</th>
                <th>Avg. Price</th>
                <th>Avg. Taste Score</th>
              </tr>
            </thead>
            <tbody>
              {districts.slice(0, 10).map((district) => (
                <tr key={district.business_district}>
                  <td>{district.business_district}</td>
                  <td>{district.count}</td>
                  <td>¥{district.avg_price?.toFixed(0) || 0}</td>
                  <td>{district.avg_taste_score?.toFixed(1) || 0}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* 价格分布 */}
      <section className="stats-section">
        <h2>Price Distribution</h2>
        <div className="table-container">
          <table className="stats-table">
            <thead>
              <tr>
                <th>Price Range</th>
                <th>Count</th>
                <th>Percentage</th>
              </tr>
            </thead>
            <tbody>
              {price_distribution.map((price) => {
                const percentage = overall.total_restaurants
                  ? ((price.count / overall.total_restaurants) * 100).toFixed(1)
                  : "0.0";
                return (
                  <tr key={price.price_range}>
                    <td>{price.price_range}</td>
                    <td>{price.count}</td>
                    <td>{percentage}%</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>

      {/* 星级统计 */}
      <section className="stats-section">
        <h2>Star Rating Distribution</h2>
        <div className="table-container">
          <table className="stats-table">
            <thead>
              <tr>
                <th>Star Rating</th>
                <th>Count</th>
                <th>Avg. Taste Score</th>
                <th>Avg. Environment Score</th>
                <th>Avg. Service Score</th>
              </tr>
            </thead>
            <tbody>
              {star_levels.map((star) => (
                <tr key={star.star_level}>
                  <td>
                    <StarRating starLevel={star.star_level} size="small" showText={true} />
                  </td>
                  <td>{star.count}</td>
                  <td>{star.avg_taste_score?.toFixed(1) || 0}</td>
                  <td>{star.avg_environment_score?.toFixed(1) || 0}</td>
                  <td>{star.avg_service_score?.toFixed(1) || 0}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* 热门餐厅 */}
      <section className="stats-section">
        <h2>Popular Restaurants (Top 10)</h2>
        <div className="table-container">
          <table className="stats-table">
            <thead>
              <tr>
                <th>Restaurant Name</th>
                <th>Cuisine Type</th>
                <th>Business District</th>
                <th>Price</th>
                <th>Taste Score</th>
                <th>Environment Score</th>
                <th>Service Score</th>
                <th>Star Rating</th>
                <th>Reviews</th>
              </tr>
            </thead>
            <tbody>
              {top_restaurants.slice(0, 10).map((restaurant) => (
                <tr key={restaurant.shop_id}>
                  <td>{restaurant.name}</td>
                  <td>{restaurant.category}</td>
                  <td>{restaurant.business_district || "-"}</td>
                  <td>¥{restaurant.avg_price || 0}</td>
                  <td>{restaurant.taste_score?.toFixed(1) || 0}</td>
                  <td>{restaurant.environment_score?.toFixed(1) || 0}</td>
                  <td>{restaurant.service_score?.toFixed(1) || 0}</td>
                  <td>
                    <StarRating starLevel={restaurant.star_level} size="small" />
                  </td>
                  <td>{restaurant.reviews || 0}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

