"""
模板种子数据。
"""

from __future__ import annotations

TEMPLATE_SEED_DATA = [
    {
        "template_id": 1,
        "title": "Guangzhou Catering Star Rating Distribution Analysis",
        "keywords": "star rating,score,industry level,data analysis",
        "default_format": "markdown",
        "content": (
            "# Guangzhou Catering Star Rating Distribution Analysis\n"
            "The Guangzhou food scene is full of hidden gems! Based on data analysis, we provide\n"
            "an in-depth look at the local catering star rating distribution pattern:\n\n"
            "### **Star Rating Distribution Overview**\n\n"
            "**Five-Star Merchant Percentage:** {percentage_five_star:.1f}% - Represents top-tier\n"
            "dining experiences\n\n"
            "**Quasi-Five-Star Merchant Percentage:** {percentage_quasi_five:.1f}% - Similarly\n"
            "excellent quality choices\n\n"
            "**Four-Star Merchant Count:** {count_four_star} establishments - Reliable quality\n"
            "despite smaller numbers\n\n"
            "### **Rating Performance by Star Level**\n\n"
            "**Five-Star Merchant Average Ratings:**\n\n"
            "**Taste:** {avg_taste_five:.1f}/10\n\n"
            "**Environment:** {avg_env_five:.1f}/10\n\n"
            "**Service:** {avg_service_five:.1f}/10\n\n"
            "**Quasi-Five-Star Merchant Average Ratings:**\n\n"
            "**Taste:** {avg_taste_quasi:.1f}/10\n\n"
            "**Environment:** {avg_env_quasi:.1f}/10\n\n"
            "**Service:** {avg_service_quasi:.1f}/10\n\n"
            "**Four-Star Merchant Highlight:** Environment and service average score reaches **\n"
            "{avg_env_service_four_star:.1f}**, showing commendable performance\n\n"
            "### **Overall Industry Standards**\n\n"
            "Guangzhou catering maintains high standards in these dimensions:\n\n"
            "**Taste:** {avg_taste_overall:.1f}/10\n\n"
            "**Environment:** {avg_env_overall:.1f}/10\n\n"
            "**Service:** {avg_service_overall:.1f}/10\n\n"
            "> *Data Insight:* Analysis based on a sample of {total_restaurants} restaurants\n"
            "shows {best_env_star_level} Merchants particularly excel in environment ratings.\n"
        ),
        "placeholders": {
            "percentage_five_star": "五星商户占比（百分比，0-100）",
            "percentage_quasi_five": "准五星商户占比（百分比，0-100）",
            "count_four_star": "四星商户数量",
            "avg_taste_five": "五星商户味道均分",
            "avg_env_five": "五星商户环境均分",
            "avg_service_five": "五星商户服务均分",
            "avg_taste_quasi": "准五星商户味道均分",
            "avg_env_quasi": "准五星商户环境均分",
            "avg_service_quasi": "准五星商户服务均分",
            "avg_env_service_four_star": "四星商户环境与服务综合均分",
            "avg_taste_overall": "全样本味道均分",
            "avg_env_overall": "全样本环境均分",
            "avg_service_overall": "全样本服务均分",
            "total_restaurants": "统计口径内餐厅数量",
            "best_env_star_level": "环境评分表现最好的星级（Five-Star/Quasi-Five-Star/Four-Star）",
        },
        "sample_output": (
            "# Guangzhou Catering Star Rating Distribution Analysis\n"
            "The Guangzhou food scene is full of hidden gems! Based on data analysis, we provide an in-\n"
            "depth look at the local catering star rating distribution pattern:\n\n"
            "### **Star Rating Distribution Overview**\n\n"
            "**Five-Star Merchant Percentage:** 32.3% - Represents top-tier dining experiences\n\n"
            "**Quasi-Five-Star Merchant Percentage:** 42.6% - Similarly excellent quality choices\n\n"
            "**Four-Star Merchant Count:** 25 establishments - Reliable quality despite smaller numbers\n\n"
            "### **Rating Performance by Star Level**\n\n"
            "**Five-Star Merchant Average Ratings:**\n\n"
            "**Taste:** 8.8/10\n\n"
            "**Environment:** 8.9/10\n\n"
            "**Service:** 8.9/10\n\n"
            "**Quasi-Five-Star Merchant Average Ratings:**\n\n"
            "**Taste:** 8.6/10\n\n"
            "**Environment:** 8.7/10\n\n"
            "**Service:** 8.7/10\n\n"
            "**Four-Star Merchant Highlight:** Environment and service average score reaches **8.3**,\n"
            "showing commendable performance\n\n"
            "### **Overall Industry Standards**\n\n"
            "Guangzhou catering maintains high standards in these dimensions:\n\n"
            "**Taste:** 8.7/10\n\n"
            "**Environment:** 8.7/10\n\n"
            "**Service:** 8.7/10\n\n"
            "> *Data Insight:* Analysis based on a sample of 93 restaurants shows Five-Star Merchants\n"
            "particularly excel in environment ratings.\n"
        ),
    },
    {
        "template_id": 2,
        "title": "Best Value Recommendations under {price_cap} Yuan",
        "keywords": "cost-performance,price ceiling,{price_cap}yuan,taste rating",
        "default_format": "markdown",
        "content": (
            "# Best Value Recommendations under {price_cap} Yuan\n"
            "Based on your budget, we've selected the {top_n} restaurants with the best value for\n"
            "money under {price_cap} yuan! (Value determined by taste rating to price ratio)\n\n"
            "**{restaurant1_name}** (Value Index: {value_for_money1:.2f})\n\n"
            "**Taste Rating:** {restaurant1_taste_score:.1f}\n\n"
            "**Avg Price:** ¥{restaurant1_price}\n\n"
            "**Recommended Dishes:** `{restaurant1_rec1}`, `{restaurant1_rec2}`\n\n"
            "**{restaurant2_name}** (Value Index: {value_for_money2:.2f})\n\n"
            "**Taste Rating:** {restaurant2_taste_score:.1f}\n\n"
            "**Avg Price:** ¥{restaurant2_price}\n\n"
            "**Recommended Dishes:** `{restaurant2_rec1}`, `{restaurant2_rec2}`\n\n"
            "**{restaurant3_name}** (Value Index: {value_for_money3:.2f})\n\n"
            "**Taste Rating:** {restaurant3_taste_score:.1f}\n\n"
            "**Avg Price:** ¥{restaurant3_price}\n\n"
            "**Recommended Dishes:** `{restaurant3_rec1}`, `{restaurant3_rec2}`\n\n"
            "**{restaurant4_name}** (Value Index: {value_for_money4:.2f})\n\n"
            "**Taste Rating:** {restaurant4_taste_score:.1f}\n\n"
            "**Avg Price:** ¥{restaurant4_price}\n\n"
            "**Recommended Dishes:** `{restaurant4_rec1}`, `{restaurant4_rec2}`\n\n"
            "**{restaurant5_name}** (Value Index: {value_for_money5:.2f})\n\n"
            "**Taste Rating:** {restaurant5_taste_score:.1f}\n\n"
            "**Avg Price:** ¥{restaurant5_price}\n\n"
            "**Recommended Dishes:** `{restaurant5_rec1}`, `{restaurant5_rec2}`\n\n"
            "> *Tip:* These restaurants provide the best taste experience on a limited budget - a\n"
            "smart choice!\n\n"
            "**Taste:** {avg_taste_overall:.1f}/10\n\n"
            "**Environment:** {avg_env_overall:.1f}/10\n\n"
            "**Service:** {avg_service_overall:.1f}/10\n\n"
            "> *Data Insight:* Analysis based on a sample of {total_restaurants} restaurants shows Five-Star Merchants particularly excel in environment ratings.\n"
        ),
        "placeholders": {
            "price_cap": "预算上限（元）",
            "top_n": "推荐数量",
            "restaurant1_name": "餐厅1名称",
            "value_for_money1": "餐厅1性价比分值",
            "restaurant1_taste_score": "餐厅1味道评分",
            "restaurant1_price": "餐厅1人均价格",
            "restaurant1_rec1": "餐厅1推荐菜1",
            "restaurant1_rec2": "餐厅1推荐菜2",
            "restaurant2_name": "餐厅2名称",
            "value_for_money2": "餐厅2性价比分值",
            "restaurant2_taste_score": "餐厅2味道评分",
            "restaurant2_price": "餐厅2人均价格",
            "restaurant2_rec1": "餐厅2推荐菜1",
            "restaurant2_rec2": "餐厅2推荐菜2",
            "restaurant3_name": "餐厅3名称",
            "value_for_money3": "餐厅3性价比分值",
            "restaurant3_taste_score": "餐厅3味道评分",
            "restaurant3_price": "餐厅3人均价格",
            "restaurant3_rec1": "餐厅3推荐菜1",
            "restaurant3_rec2": "餐厅3推荐菜2",
            "restaurant4_name": "餐厅4名称",
            "value_for_money4": "餐厅4性价比分值",
            "restaurant4_taste_score": "餐厅4味道评分",
            "restaurant4_price": "餐厅4人均价格",
            "restaurant4_rec1": "餐厅4推荐菜1",
            "restaurant4_rec2": "餐厅4推荐菜2",
            "restaurant5_name": "餐厅5名称",
            "value_for_money5": "餐厅5性价比分值",
            "restaurant5_taste_score": "餐厅5味道评分",
            "restaurant5_price": "餐厅5人均价格",
            "restaurant5_rec1": "餐厅5推荐菜1",
            "restaurant5_rec2": "餐厅5推荐菜2",
            "avg_taste_overall": "整体味道评分均值",
            "avg_env_overall": "整体环境评分均值",
            "avg_service_overall": "整体服务评分均值",
            "total_restaurants": "统计样本数量",
        },
    },
    {
        "template_id": 4,
        "title": "Alleyway Surprises: Discovering Small, High-Rated Restaurants in {district} District",
        "keywords": "small,high value,treasure stores,{district}",
        "default_format": "markdown",
        "content": (
            "# Alleyway Surprises: Discovering Small, High-Rated Restaurants in {district} District\n\n"
            "Tired of crowded stores? The {district} district hides some treasure restaurants\n"
            "that are less reviewed but highly rated! They might be less conspicuous but could\n"
            "offer unexpected delights:\n\n"
            "**{gem_name}**\n\n"
            "**Type:** {gem_category}\n\n"
            "**Rating:** **{gem_score:.1f}** (Taste:{gem_taste} Environment:{gem_env} Service:\n"
            "{gem_service})\n\n"
            "**Avg Price:** ¥{gem_price} (Great value)\n\n"
            "**Highlights:** Owner recommends `{gem_rec1}` and `{gem_rec2}`, reportedly\n"
            "{gem_highlight}.\n\n"
            "**Address:** {gem_address}\n"
        ),
        "placeholders": {
            "district": "商圈/区域名称",
            "gem_name": "宝藏餐厅名称",
            "gem_category": "餐厅类型",
            "gem_score": "综合评分",
            "gem_taste": "味道评分",
            "gem_env": "环境评分",
            "gem_service": "服务评分",
            "gem_price": "人均价格",
            "gem_rec1": "推荐菜1",
            "gem_rec2": "推荐菜2",
            "gem_highlight": "亮点描述",
            "gem_address": "地址",
        },
    },
    {
        "template_id": 5,
        "title": "District Food Express: {district}",
        "keywords": "overview,popular cuisines,average price,highly rated stores",
        "default_format": "html",
        "content": (
            "<h2>District Food Express: {district}</h2>\n\n"
            "<p>In the vibrant <strong>{district}</strong> business district, the food map is\n"
            "being refreshed! Data insights show:\n\n"
            "The main consumption driver here is <strong>{most_common_category}</strong> cuisine\n"
            "(accounting for {most_common_category_percentage:.1f}%),\n"
            "while also offering diverse choices like <strong>{distinct_category}</strong>.</p>\n\n"
            "<p>The overall consumption level is affordable, averaging about <strong>\n"
            "{avg_price_district:.1f}</strong> yuan.\n"
            "The most notable highly-rated representatives include:</p>\n\n"
            "<ul>\n"
            "<li><strong>{restaurant1_name}</strong> (Comprehensive Rating:\n"
            "{restaurant1_score:.1f})</li>\n"
            "<li><strong>{restaurant2_name}</strong> (Comprehensive Rating:\n"
            "{restaurant2_score:.1f})</li>\n"
            "</ul>\n\n"
            "<p><strong>Dining Tip:</strong> The peak dining hours in this district are\n"
            "concentrated between 18:00-19:30, it's advised to make reservations in advance for\n"
            "popular stores like {restaurant1_name}.</p>\n"
            "<!-- Optional: Business district heatmap anchor point -->\n"
        ),
        "placeholders": {
            "district": "商圈/区域名称",
            "most_common_category": "最常见菜系",
            "most_common_category_percentage": "主流菜系占比（百分比）",
            "distinct_category": "特色菜系或差异菜系",
            "avg_price_district": "区域平均人均消费",
            "restaurant1_name": "推荐餐厅1名称",
            "restaurant1_score": "推荐餐厅1综合评分",
            "restaurant2_name": "推荐餐厅2名称",
            "restaurant2_score": "推荐餐厅2综合评分",
        },
    },
    {
        "template_id": 6,
        "title": "Food at Home: Top Rated Delivery Picks in {district} District",
        "keywords": "delivery,home,convenient,high rating",
        "default_format": "markdown",
        "content": (
            "# Food at Home: Top Rated Delivery Picks in {district} District\n\n"
            "Enjoy the deliciousness of the **{district}** district without leaving home! We've\n"
            "selected several restaurants with **high comprehensive ratings ({min_score}+)**\n"
            "suitable for delivery:\n\n"
            "**{restaurant1_name} ({restaurant1_score:.1f})** - {restaurant1_category}\n\n"
            "**Avg. Price:** ¥{restaurant1_price}\n\n"
            "**Signature Delivery Dishes:** `{restaurant1_rec1}`, `{restaurant1_rec2}`\n\n"
            "**{restaurant2_name} ({restaurant2_score:.1f})** - {restaurant2_category}\n\n"
            "**Avg. Price:** ¥{restaurant2_price}\n\n"
            "**Signature Delivery Dishes:** `{restaurant2_rec1}`, `{restaurant2_rec2}`\n\n"
            "**{restaurant3_name} ({restaurant3_score:.1f})** - {restaurant3_category}\n\n"
            "**Avg. Price:** ¥{restaurant3_price}\n\n"
            "**Signature Delivery Dishes:** `{restaurant3_rec1}`, `{restaurant3_rec2}`\n\n"
            "> *Tip:* The above restaurants excel in both **Taste ({avg_taste_score:.1f})** and\n"
            "**Service ({avg_service_score:.1f})**, making them great choices for delivery!\n"
        ),
        "placeholders": {
            "district": "商圈/区域名称",
            "min_score": "最低综合评分阈值",
            "restaurant1_name": "外卖推荐餐厅1名称",
            "restaurant1_score": "餐厅1综合评分",
            "restaurant1_category": "餐厅1菜系",
            "restaurant1_price": "餐厅1人均价格",
            "restaurant1_rec1": "餐厅1推荐菜1",
            "restaurant1_rec2": "餐厅1推荐菜2",
            "restaurant2_name": "外卖推荐餐厅2名称",
            "restaurant2_score": "餐厅2综合评分",
            "restaurant2_category": "餐厅2菜系",
            "restaurant2_price": "餐厅2人均价格",
            "restaurant2_rec1": "餐厅2推荐菜1",
            "restaurant2_rec2": "餐厅2推荐菜2",
            "restaurant3_name": "外卖推荐餐厅3名称",
            "restaurant3_score": "餐厅3综合评分",
            "restaurant3_category": "餐厅3菜系",
            "restaurant3_price": "餐厅3人均价格",
            "restaurant3_rec1": "餐厅3推荐菜1",
            "restaurant3_rec2": "餐厅3推荐菜2",
            "avg_taste_score": "筛选样本味道均分",
            "avg_service_score": "筛选样本服务均分",
        },
    },
    {
        "template_id": 7,
        "title": "Guangzhou Food Statistics Visualization Report",
        "keywords": "statistics,visualization,data analysis,charts",
        "default_format": "html",
        "content": (
            "<h1>Guangzhou Food Statistics Visualization Report</h1>\n\n"
            "<h2>Overall Statistics</h2>\n"
            "<p>This report provides comprehensive statistics and visual analysis of Guangzhou's food scene:</p>\n"
            "<ul>\n"
            "<li><strong>Total Restaurants:</strong> {total_restaurants}</li>\n"
            "<li><strong>Total Cuisine Types:</strong> {total_categories}</li>\n"
            "<li><strong>Total Business Districts:</strong> {total_districts}</li>\n"
            "<li><strong>Average Price:</strong> ¥{avg_price:.1f}</li>\n"
            "<li><strong>Average Taste Score:</strong> {avg_taste_score:.1f}/10</li>\n"
            "<li><strong>Average Environment Score:</strong> {avg_environment_score:.1f}/10</li>\n"
            "<li><strong>Average Service Score:</strong> {avg_service_score:.1f}/10</li>\n"
            "<li><strong>Total Reviews:</strong> {total_reviews:,}</li>\n"
            "</ul>\n\n"
            "<h2>Category Distribution (Top 10)</h2>\n"
            "<div class=\"chart-container\"><canvas id=\"categoryChart\"></canvas></div>\n\n"
            "<h2>Business District Distribution (Top 10)</h2>\n"
            "<div class=\"chart-container\"><canvas id=\"districtChart\"></canvas></div>\n\n"
            "<h2>Price Distribution</h2>\n"
            "<div class=\"chart-container\"><canvas id=\"priceChart\"></canvas></div>\n\n"
            "<h2>Star Rating Distribution</h2>\n"
            "<div class=\"chart-container\"><canvas id=\"starChart\"></canvas></div>\n\n"
            "<h2>Summary</h2>\n"
            "<p>This comprehensive report provides insights into Guangzhou's food industry through data visualization. "
            "The charts above illustrate the distribution patterns across categories, districts, price ranges, and star ratings, "
            "helping to understand the overall market landscape.</p>\n"
        ),
        "placeholders": {
            "total_restaurants": "餐厅总数",
            "total_categories": "菜系种类数",
            "total_districts": "商圈数量",
            "avg_price": "平均价格",
            "avg_taste_score": "平均味道评分",
            "avg_environment_score": "平均环境评分",
            "avg_service_score": "平均服务评分",
            "total_reviews": "总评论数",
            "category_labels_json": "菜系标签JSON数组",
            "category_counts_json": "菜系数量JSON数组",
            "district_labels_json": "商圈标签JSON数组",
            "district_counts_json": "商圈数量JSON数组",
            "price_labels_json": "价格区间标签JSON数组",
            "price_counts_json": "价格区间数量JSON数组",
            "star_labels_json": "星级标签JSON数组",
            "star_counts_json": "星级数量JSON数组",
        },
    },
]


