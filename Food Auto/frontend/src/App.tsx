import { useState } from "react";
import { useRestaurants } from "./hooks/useRestaurants";
import { RestaurantTable } from "./components/RestaurantTable";
import { RestaurantFiltersComponent } from "./components/RestaurantFilters";
import { RestaurantDetail } from "./components/RestaurantDetail";
import { Pagination } from "./components/Pagination";
import { Navigation, type PageType } from "./components/Navigation";
import { Dashboard } from "./components/Dashboard";
import { TemplateManagement } from "./components/TemplateManagement";
import { ReportGenerator } from "./components/ReportGenerator";
import { ThemeToggle } from "./components/ThemeToggle";
import { ToastContainer, useToast } from "./components/Toast";
import { restaurantApi } from "./api/restaurants";
import type { SortField, SortOrder, Restaurant } from "./types";

function App() {
  const [currentPage, setCurrentPage] = useState<PageType>("list");
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [selectedRestaurant, setSelectedRestaurant] = useState<Restaurant | null>(null);
  const [showDetail, setShowDetail] = useState(false);
  const { toasts, showToast, removeToast } = useToast();
  
  const {
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
    refetch,
  } = useRestaurants({ initialLimit: 20, initialPage: 1 });

  // 当筛选条件改变时，重置到第一页（已在 updateFilters 中处理）
  const handleFiltersChange = (newFilters: typeof filters) => {
    updateFilters(newFilters);
  };

  const handlePageChange = (newPage: number) => {
    updatePage(newPage);
    // 滚动到顶部
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleLimitChange = (newLimit: number) => {
    updateLimit(newLimit);
  };

  const handleBatchDelete = async () => {
    if (selectedIds.length === 0) {
      showToast("Please select restaurants to delete first", "warning");
      return;
    }
    if (!confirm(`Are you sure you want to delete ${selectedIds.length} selected restaurant(s)?`)) {
      return;
    }
    try {
      await restaurantApi.batchOperation("delete", selectedIds);
      showToast(`Successfully deleted ${selectedIds.length} restaurant(s)`, "success");
      setSelectedIds([]);
      // 刷新数据
      refetch();
    } catch (error) {
      showToast("Delete failed: " + (error as Error).message, "error");
    }
  };

  const handleRowClick = (restaurant: Restaurant) => {
    setSelectedRestaurant(restaurant);
    setShowDetail(true);
  };

  const handleDetailClose = () => {
    setShowDetail(false);
    setSelectedRestaurant(null);
  };

  const handleDetailUpdate = () => {
    // 刷新数据
    refetch();
    setShowDetail(false);
    setSelectedRestaurant(null);
  };

  // 处理初始化错误
  if (error && restaurants.length === 0 && !loading) {
    return (
      <main className="container">
        <header>
          <div className="header-content">
            <div>
              <h1>Guangzhou Food Content Management System</h1>
              <p>Manage Guangzhou restaurant data with filtering, search, sorting, and pagination</p>
            </div>
            <ThemeToggle />
          </div>
        </header>
        <div className="error-banner">
          <p className="error">Failed to load: {error}</p>
          <p style={{ marginTop: "1rem", fontSize: "0.875rem", color: "#64748b" }}>
            Please ensure the backend service is running at http://localhost:8000
          </p>
        </div>
      </main>
    );
  }

  if (currentPage === "dashboard") {
    return (
      <main className="container">
        <header>
          <div className="header-content">
            <div>
              <h1>Guangzhou Food Content Management System</h1>
              <p>Manage Guangzhou restaurant data with filtering, search, sorting, and pagination</p>
            </div>
            <ThemeToggle />
          </div>
        </header>
        <Navigation currentPage={currentPage} onNavigate={setCurrentPage} />
        <Dashboard />
      </main>
    );
  }

  if (currentPage === "templates") {
    return (
      <main className="container">
        <header>
          <div className="header-content">
            <div>
              <h1>Guangzhou Food Content Management System</h1>
              <p>Manage Guangzhou restaurant data with filtering, search, sorting, and pagination</p>
            </div>
            <ThemeToggle />
          </div>
        </header>
        <Navigation currentPage={currentPage} onNavigate={setCurrentPage} />
        <section className="table-section">
          <TemplateManagement />
        </section>
      </main>
    );
  }

  if (currentPage === "reports") {
    return (
      <main className="container">
        <header>
          <div className="header-content">
            <div>
              <h1>Guangzhou Food Content Management System</h1>
              <p>Manage Guangzhou restaurant data with filtering, search, sorting, and pagination</p>
            </div>
            <ThemeToggle />
          </div>
        </header>
        <Navigation currentPage={currentPage} onNavigate={setCurrentPage} />
        <section className="table-section">
          <ReportGenerator />
        </section>
      </main>
    );
  }

  return (
    <main className="container">
      <header>
        <div className="header-content">
          <div>
            <h1>Guangzhou Food Content Management System</h1>
            <p>Manage Guangzhou restaurant data with filtering, search, sorting, and pagination</p>
          </div>
          <ThemeToggle />
        </div>
      </header>
      <Navigation currentPage={currentPage} onNavigate={setCurrentPage} />

      {error && (
        <div className="error-banner">
          <p className="error">{error}</p>
        </div>
      )}

      <RestaurantFiltersComponent
        filters={filters}
        onFiltersChange={handleFiltersChange}
        categories={categories}
        districts={districts}
        starLevels={starLevels}
      />

      <section className="table-section">
        <div className="table-header">
          <h2>Restaurant List</h2>
          <div className="table-header-actions">
            <div className="table-stats">
              {loading
                ? "Loading..."
                : total > 0
                ? `Showing ${restaurants.length} / ${total} restaurant(s)${totalPages > 0 ? ` (Page ${page} / ${totalPages})` : ""}`
                : "No data"}
            </div>
            <div className="table-actions">
              {selectedIds.length > 0 && (
                <div className="batch-actions">
                  <span className="selected-count">{selectedIds.length} selected</span>
                  <button
                    className="btn btn-danger btn-sm"
                    onClick={handleBatchDelete}
                  >
                    Batch Delete
                  </button>
                </div>
              )}
              <div className="export-buttons">
                <button
                  className="btn btn-secondary btn-sm"
                  onClick={async () => {
                    try {
                      const blob = await restaurantApi.exportCSV(filters);
                      const url = window.URL.createObjectURL(blob);
                      const a = document.createElement("a");
                      a.href = url;
                      a.download = "restaurants.csv";
                      a.click();
                      window.URL.revokeObjectURL(url);
                      showToast("CSV exported successfully", "success");
                    } catch (error) {
                      showToast("Export failed: " + (error as Error).message, "error");
                    }
                  }}
                >
                  Export CSV
                </button>
                <button
                  className="btn btn-secondary btn-sm"
                  onClick={async () => {
                    try {
                      const blob = await restaurantApi.exportExcel(filters);
                      const url = window.URL.createObjectURL(blob);
                      const a = document.createElement("a");
                      a.href = url;
                      a.download = "restaurants.xlsx";
                      a.click();
                      window.URL.revokeObjectURL(url);
                      showToast("Excel exported successfully", "success");
                    } catch (error) {
                      showToast("Export failed: " + (error as Error).message, "error");
                    }
                  }}
                >
                  Export Excel
                </button>
              </div>
            </div>
          </div>
        </div>

        <RestaurantTable
          restaurants={restaurants}
          loading={loading}
          onSort={(field: SortField, order: SortOrder) => handleSort(field, order)}
          onSelect={setSelectedIds}
          onRowClick={handleRowClick}
          selectedIds={selectedIds}
        />

        {!loading && total > 0 && totalPages > 0 && (
          <Pagination
            currentPage={page}
            totalPages={totalPages}
            total={total}
            limit={limit}
            onPageChange={handlePageChange}
            onLimitChange={handleLimitChange}
          />
        )}
      </section>

      {showDetail && selectedRestaurant && (
        <RestaurantDetail
          shopId={selectedRestaurant.shop_id}
          onClose={handleDetailClose}
          onUpdate={handleDetailUpdate}
        />
      )}

      <ToastContainer toasts={toasts} onRemove={removeToast} />
    </main>
  );
}

export default App;


