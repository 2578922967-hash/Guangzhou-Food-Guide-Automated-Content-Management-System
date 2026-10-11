// 星级评分组件

interface StarRatingProps {
  starLevel: string | null | undefined;
  size?: "small" | "medium" | "large";
  showText?: boolean;
}

export function StarRating({ starLevel, size = "medium", showText = false }: StarRatingProps) {
  if (!starLevel) {
    return <span>-</span>;
  }

  // 解析星级文本，转换为星数
  const getStarCount = (level: string): number => {
    const levelLower = level.toLowerCase().trim();
    
    // 准五星商户 (Quasi five-star merchant) - 必须先检查，否则会被"five-star merchant"匹配
    if (levelLower.includes("quasi five") || 
        levelLower.includes("quasi-five") ||
        levelLower.includes("准五星") ||
        levelLower === "准5星") {
      return 4.5;
    }
    
    // 准四星商户 (Quasi four-star merchant) - 必须先检查，否则会被"four-star merchant"匹配
    if (levelLower.includes("quasi four") || 
        levelLower.includes("quasi-four") ||
        levelLower.includes("准四星") ||
        levelLower === "准4星") {
      return 3.5;
    }
    
    // 准三星商户 - 必须先检查
    if (levelLower.includes("quasi three") || 
        levelLower.includes("quasi-three") ||
        levelLower.includes("准三星") ||
        levelLower === "准3星") {
      return 2.5;
    }
    
    // 准二星商户 - 必须先检查
    if (levelLower.includes("quasi two") || 
        levelLower.includes("quasi-two") ||
        levelLower.includes("准二星") ||
        levelLower === "准2星") {
      return 1.5;
    }
    
    // 准一星商户 - 必须先检查
    if (levelLower.includes("quasi one") || 
        levelLower.includes("quasi-one") ||
        levelLower.includes("准一星") ||
        levelLower === "准1星") {
      return 0.5;
    }
    
    // 五星商户 (Five-star merchant)
    if (levelLower.includes("five-star merchant") || 
        levelLower === "five-star" || 
        levelLower.includes("五星商户") ||
        levelLower === "五星") {
      return 5;
    }
    
    // 四星商户 (Four-star merchant)
    if (levelLower.includes("four-star merchant") || 
        levelLower.includes("four-star") ||
        levelLower === "four star" ||
        levelLower.includes("四星商户") ||
        levelLower === "四星") {
      return 4;
    }
    
    // 三星商户
    if (levelLower.includes("three-star") || 
        levelLower.includes("three star") ||
        levelLower.includes("三星商户") ||
        levelLower === "三星") {
      return 3;
    }
    
    // 二星商户
    if (levelLower.includes("two-star") || 
        levelLower.includes("two star") ||
        levelLower.includes("二星商户") ||
        levelLower === "二星") {
      return 2;
    }
    
    // 一星商户
    if (levelLower.includes("one-star") || 
        levelLower.includes("one star") ||
        levelLower.includes("一星商户") ||
        levelLower === "一星") {
      return 1;
    }
    
    // 默认值，如果没有匹配到
    return 0;
  };

  const starCount = getStarCount(starLevel);
  
  // 如果无法识别星级，显示原文本
  if (starCount === 0) {
    return <span>{starLevel}</span>;
  }

  const sizeClasses = {
    small: "star-rating-small",
    medium: "star-rating-medium",
    large: "star-rating-large",
  };

  const fullStars = Math.floor(starCount);
  const hasHalfStar = starCount % 1 !== 0;
  const emptyStars = 5 - Math.ceil(starCount);

  return (
    <div className={`star-rating ${sizeClasses[size]}`} title={starLevel}>
      <span className="star-rating-icons">
        {Array.from({ length: fullStars }).map((_, i) => (
          <span key={`full-${i}`} className="star-icon star-full" aria-label="Full star">
            ★
          </span>
        ))}
        {hasHalfStar && (
          <span className="star-icon star-half" aria-label="Half star" title={starLevel}>
            <span className="star-half-empty">☆</span>
            <span className="star-half-full"></span>
          </span>
        )}
        {Array.from({ length: emptyStars }).map((_, i) => (
          <span key={`empty-${i}`} className="star-icon star-empty" aria-label="Empty star">
            ☆
          </span>
        ))}
      </span>
      {showText && <span className="star-rating-text">{starLevel}</span>}
    </div>
  );
}
