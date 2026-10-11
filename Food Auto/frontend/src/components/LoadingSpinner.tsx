// 加载动画组件

interface LoadingSpinnerProps {
  size?: "small" | "medium" | "large";
  text?: string;
}

export function LoadingSpinner({ size = "medium", text }: LoadingSpinnerProps) {
  const sizeClasses = {
    small: "spinner-small",
    medium: "spinner-medium",
    large: "spinner-large",
  };

  return (
    <div className="loading-spinner-container">
      <div className={`loading-spinner ${sizeClasses[size]}`}></div>
      {text && <p className="loading-text">{text}</p>}
    </div>
  );
}

// 骨架屏组件
interface SkeletonProps {
  width?: string;
  height?: string;
  className?: string;
}

export function Skeleton({ width = "100%", height = "1rem", className = "" }: SkeletonProps) {
  return (
    <div
      className={`skeleton ${className}`}
      style={{ width, height }}
    ></div>
  );
}

export function SkeletonCard() {
  return (
    <div className="skeleton-card">
      <Skeleton width="60%" height="1.5rem" />
      <Skeleton width="40%" height="1rem" className="skeleton-margin" />
      <Skeleton width="30%" height="1rem" />
    </div>
  );
}

export function SkeletonTable() {
  return (
    <div className="skeleton-table">
      <Skeleton height="2rem" className="skeleton-margin" />
      {Array.from({ length: 5 }).map((_, i) => (
        <Skeleton key={i} height="3rem" className="skeleton-margin" />
      ))}
    </div>
  );
}

