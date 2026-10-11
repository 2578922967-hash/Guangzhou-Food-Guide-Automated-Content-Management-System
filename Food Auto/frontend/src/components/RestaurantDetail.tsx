// 餐厅详情组件

import { useState, useEffect } from "react";
import { restaurantApi } from "../api/restaurants";
import type { Restaurant } from "../types";
import { StarRating } from "./StarRating";

interface RestaurantDetailProps {
  shopId: string;
  onClose: () => void;
  onUpdate?: () => void;
}

export function RestaurantDetail({ shopId, onClose, onUpdate }: RestaurantDetailProps) {
  const [restaurant, setRestaurant] = useState<Restaurant | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState<Partial<Restaurant>>({});

  useEffect(() => {
    const fetchRestaurant = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await restaurantApi.getRestaurant(shopId);
        setRestaurant(data);
        setFormData(data);
      } catch (err: any) {
        setError(err.message || "Failed to load");
      } finally {
        setLoading(false);
      }
    };
    fetchRestaurant();
  }, [shopId]);

  const handleSave = async () => {
    if (!restaurant) return;
    
    try {
      await restaurantApi.updateRestaurant(shopId, formData);
      const updated = await restaurantApi.getRestaurant(shopId);
      setRestaurant(updated);
      setFormData(updated);
      setEditing(false);
      onUpdate?.();
    } catch (err: any) {
      alert("Update failed: " + (err.message || "Unknown error"));
    }
  };

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this restaurant? This action cannot be undone!")) return;
    
    try {
      await restaurantApi.deleteRestaurant(shopId);
      onClose();
      onUpdate?.();
    } catch (err: any) {
      alert("Delete failed: " + (err.message || "Unknown error"));
    }
  };

  if (loading) {
    return (
      <div className="detail-modal">
        <div className="detail-content">
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  if (error || !restaurant) {
    return (
      <div className="detail-modal">
        <div className="detail-content">
          <div className="error-banner">
            <p className="error">{error || "Restaurant not found"}</p>
          </div>
          <button className="btn btn-secondary" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="detail-modal" onClick={onClose}>
      <div className="detail-content" onClick={(e) => e.stopPropagation()}>
        <div className="detail-header">
          <h2>{restaurant.name}</h2>
          <button className="close-button" onClick={onClose} aria-label="Close">
            ×
          </button>
        </div>

        <div className="detail-body">
          {editing ? (
            <div className="detail-form">
              <div className="form-group">
                <label>Restaurant Name</label>
                <input
                  type="text"
                  value={formData.name || ""}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label>Cuisine Type</label>
                <input
                  type="text"
                  value={formData.category || ""}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label>Business District</label>
                <input
                  type="text"
                  value={formData.business_district || ""}
                  onChange={(e) => setFormData({ ...formData, business_district: e.target.value })}
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label>Address</label>
                <input
                  type="text"
                  value={formData.address || ""}
                  onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label>Average Price</label>
                <input
                  type="number"
                  value={formData.avg_price || ""}
                  onChange={(e) => setFormData({ ...formData, avg_price: Number(e.target.value) })}
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label>Taste Score</label>
                <input
                  type="number"
                  step="0.1"
                  min="0"
                  max="10"
                  value={formData.taste_score || ""}
                  onChange={(e) => setFormData({ ...formData, taste_score: Number(e.target.value) })}
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label>Environment Score</label>
                <input
                  type="number"
                  step="0.1"
                  min="0"
                  max="10"
                  value={formData.environment_score || ""}
                  onChange={(e) => setFormData({ ...formData, environment_score: Number(e.target.value) })}
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label>Service Score</label>
                <input
                  type="number"
                  step="0.1"
                  min="0"
                  max="10"
                  value={formData.service_score || ""}
                  onChange={(e) => setFormData({ ...formData, service_score: Number(e.target.value) })}
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label>Star Rating</label>
                <input
                  type="text"
                  value={formData.star_level || ""}
                  onChange={(e) => setFormData({ ...formData, star_level: e.target.value })}
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label>Reviews</label>
                <input
                  type="number"
                  value={formData.reviews || ""}
                  onChange={(e) => setFormData({ ...formData, reviews: Number(e.target.value) })}
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label>Recommended Dish 1</label>
                <input
                  type="text"
                  value={formData.recommended_dish_1 || ""}
                  onChange={(e) => setFormData({ ...formData, recommended_dish_1: e.target.value })}
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label>Recommended Dish 2</label>
                <input
                  type="text"
                  value={formData.recommended_dish_2 || ""}
                  onChange={(e) => setFormData({ ...formData, recommended_dish_2: e.target.value })}
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label>Recommended Dish 3</label>
                <input
                  type="text"
                  value={formData.recommended_dish_3 || ""}
                  onChange={(e) => setFormData({ ...formData, recommended_dish_3: e.target.value })}
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label>URL</label>
                <input
                  type="url"
                  value={formData.url || ""}
                  onChange={(e) => setFormData({ ...formData, url: e.target.value })}
                  className="form-input"
                />
              </div>

              <div className="form-actions">
                <button className="btn btn-primary" onClick={handleSave}>
                  Save
                </button>
                <button className="btn btn-secondary" onClick={() => {
                  setFormData(restaurant);
                  setEditing(false);
                }}>
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <div className="detail-info">
              <div className="info-row">
                <span className="info-label">Shop ID:</span>
                <span className="info-value">{restaurant.shop_id}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Cuisine Type:</span>
                <span className="info-value">{restaurant.category}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Business District:</span>
                <span className="info-value">{restaurant.business_district || "-"}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Address:</span>
                <span className="info-value">{restaurant.address || "-"}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Average Price:</span>
                <span className="info-value">¥{restaurant.avg_price || 0}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Taste Score:</span>
                <span className="info-value">{restaurant.taste_score?.toFixed(1) || "-"}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Environment Score:</span>
                <span className="info-value">{restaurant.environment_score?.toFixed(1) || "-"}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Service Score:</span>
                <span className="info-value">{restaurant.service_score?.toFixed(1) || "-"}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Star Rating:</span>
                <span className="info-value">
                  <StarRating starLevel={restaurant.star_level} size="medium" showText={true} />
                </span>
              </div>
              <div className="info-row">
                <span className="info-label">Reviews:</span>
                <span className="info-value">{restaurant.reviews || 0}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Recommended Dish 1:</span>
                <span className="info-value">{restaurant.recommended_dish_1 || "-"}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Recommended Dish 2:</span>
                <span className="info-value">{restaurant.recommended_dish_2 || "-"}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Recommended Dish 3:</span>
                <span className="info-value">{restaurant.recommended_dish_3 || "-"}</span>
              </div>
              {restaurant.url && (
                <div className="info-row">
                  <span className="info-label">URL:</span>
                  <a href={restaurant.url} target="_blank" rel="noopener noreferrer" className="info-link">
                    {restaurant.url}
                  </a>
                </div>
              )}

              <div className="detail-actions">
                <button className="btn btn-primary" onClick={() => setEditing(true)}>
                  Edit
                </button>
                <button className="btn btn-secondary" onClick={handleDelete}>
                  Delete
                </button>
                <button className="btn btn-secondary" onClick={onClose}>
                  Close
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

