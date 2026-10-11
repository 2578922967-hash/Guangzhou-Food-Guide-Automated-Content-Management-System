PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS restaurants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_id TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    reviews INTEGER DEFAULT 0,
    avg_price REAL,
    category TEXT NOT NULL,
    business_district TEXT,
    address TEXT,
    recommended_dish_1 TEXT,
    recommended_dish_2 TEXT,
    recommended_dish_3 TEXT,
    taste_score REAL,
    environment_score REAL,
    service_score REAL,
    star_level TEXT,
    url TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS templates (
    template_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    keywords TEXT,
    default_format TEXT NOT NULL CHECK (default_format IN ('text', 'markdown', 'html')),
    content TEXT NOT NULL,
    placeholders_json TEXT NOT NULL,
    sample_output TEXT,
    version INTEGER DEFAULT 1,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reports (
    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_id INTEGER NOT NULL REFERENCES templates(template_id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    params_json TEXT NOT NULL,
    content_text TEXT,
    content_markdown TEXT,
    content_html TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_restaurants_category ON restaurants(category);
CREATE INDEX IF NOT EXISTS idx_restaurants_district ON restaurants(business_district);
CREATE INDEX IF NOT EXISTS idx_restaurants_star_level ON restaurants(star_level);
CREATE INDEX IF NOT EXISTS idx_restaurants_avg_price ON restaurants(avg_price);

CREATE INDEX IF NOT EXISTS idx_templates_title ON templates(title);
CREATE INDEX IF NOT EXISTS idx_templates_keywords ON templates(keywords);

CREATE INDEX IF NOT EXISTS idx_reports_template_id ON reports(template_id);

CREATE TRIGGER IF NOT EXISTS trg_restaurants_updated_at
AFTER UPDATE ON restaurants
FOR EACH ROW
BEGIN
    UPDATE restaurants SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_templates_updated_at
AFTER UPDATE ON templates
FOR EACH ROW
BEGIN
    UPDATE templates SET updated_at = CURRENT_TIMESTAMP WHERE template_id = OLD.template_id;
END;

