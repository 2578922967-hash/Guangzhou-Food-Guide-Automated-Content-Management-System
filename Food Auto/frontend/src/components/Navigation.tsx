// 导航组件

export type PageType = "list" | "dashboard" | "templates" | "reports";

interface NavigationProps {
  currentPage: PageType;
  onNavigate: (page: PageType) => void;
}

export function Navigation({ currentPage, onNavigate }: NavigationProps) {
  return (
    <nav className="navigation">
      <div className="nav-links">
        <button
          className={`nav-link ${currentPage === "list" ? "active" : ""}`}
          onClick={() => onNavigate("list")}
        >
          Restaurant List
        </button>
        <button
          className={`nav-link ${currentPage === "dashboard" ? "active" : ""}`}
          onClick={() => onNavigate("dashboard")}
        >
          Statistics
        </button>
        <button
          className={`nav-link ${currentPage === "templates" ? "active" : ""}`}
          onClick={() => onNavigate("templates")}
        >
          Template Management
        </button>
        <button
          className={`nav-link ${currentPage === "reports" ? "active" : ""}`}
          onClick={() => onNavigate("reports")}
        >
          Report Generator
        </button>
      </div>
    </nav>
  );
}

