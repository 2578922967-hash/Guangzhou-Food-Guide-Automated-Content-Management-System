# 广州美食内容管理系统 (GZ-FoodCMS)

## 快速开始

### 1. 后端启动

```bash
# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库（首次运行）
python -m src.cli init-db --seed

# 启动 Flask 后端
python -m src.app
```

后端将在 `http://localhost:8000` 运行

### 2. 前端启动

```bash
cd frontend

# 安装依赖（首次运行）
npm install

# 启动开发服务器
cd /Users/ljh2578922967/code/Food\ Auto/frontend
npm run dev
```

前端将在 `http://localhost:5173` 运行

## 排查连接问题

如果前端显示"无法连接到后端"，请按以下步骤检查：

1. **确认后端已启动**
   ```bash
   # 在浏览器访问
   http://localhost:8000/api/health
   # 应该返回: {"status": "ok"}
   ```

2. **检查后端端口**
   - 后端应该在 8000 端口运行
   - 前端代理配置在 `frontend/vite.config.ts` 中

3. **检查 CORS 设置**
   - 后端已启用 CORS (`flask-cors`)
   - 如果仍有问题，检查 `src/api/__init__.py`

4. **查看浏览器控制台**
   - 打开浏览器开发者工具（F12）
   - 查看 Console 和 Network 标签
   - 检查是否有 CORS 错误或网络错误

5. **直接测试 API**
   ```bash
   # 使用 curl 测试
   curl http://localhost:8000/api/health
   curl "http://localhost:8000/api/restaurants/?limit=5"
   ```

## 功能说明

### 前端功能

1. **餐厅列表管理**
   - 查看餐厅列表（支持分页）
   - 筛选餐厅（按名称、菜系、商圈、星级、价格、评分等）
   - 排序餐厅（按名称、价格、评分、评论数等）
   - 搜索餐厅（实时搜索，支持防抖）

2. **餐厅详情**
   - 查看餐厅详细信息
   - 编辑餐厅信息
   - 删除餐厅（软删除）

3. **批量操作**
   - 批量选择餐厅（复选框）
   - 批量删除餐厅

4. **数据导出**
   - 导出 CSV（支持筛选条件）
   - 导出 Excel（支持筛选条件，带格式）

5. **数据统计**
   - 总体统计（餐厅总数、分类数、商圈数、平均价格、平均评分等）
   - 菜系统计（各菜系的餐厅数量、平均价格、平均评分）
   - 商圈统计（各商圈的餐厅数量、平均价格、平均评分）
   - 价格分布（价格区间分布）
   - 星级统计（各星级的餐厅数量和平均评分）
   - 热门餐厅（按评分、评论数等排序）

6. **暗色模式**
   - 支持亮色/暗色主题切换
   - 主题设置持久化（localStorage）
   - 自动检测系统主题偏好

7. **模板管理**
   - 查看模板列表（左侧卡片列表）
   - 查看模板详情（右侧详情面板）
   - 编辑模板（标题、关键词、格式、内容、占位符、示例输出）
   - 删除模板

8. **报告生成**
   - 选择模板（6 个预定义模板）
   - 设置参数（根据模板要求）：
     - 模板 1：无需参数（星级分布分析）
     - 模板 2：价格上限、推荐数量（性价比推荐）
     - 模板 3：商圈（冬季暖胃）
     - 模板 4：商圈（隐藏宝藏）
     - 模板 5：商圈（商圈美食速览）
     - 模板 6：商圈、最低评分（外卖推荐）
   - 选择输出格式（文本、Markdown、HTML）
   - 生成报告
   - 切换格式查看报告（文本、Markdown、HTML）
   - 复制报告内容
   - 下载报告文件
   - 保存报告到数据库（可选）

9. **UI/UX 优化**
   - Toast 通知系统（替代 alert）
   - 加载动画和骨架屏
   - 表格斑马纹和 hover 效果
   - 按钮动画和交互反馈
   - 卡片悬停效果
   - 淡入动画
   - 响应式设计优化
   - 暗色模式支持

### CLI 命令

```bash
# 初始化数据库
python -m src.cli init-db --seed

# 导入 CSV 数据
python -m src.cli import-restaurants data/GuangZhou_food.csv

# 查询餐厅
python -m src.cli list-restaurants --category 粤菜 --limit 10

# 生成报告
python -m src.cli generate-report --template-id 1 --format markdown

# 启动文本菜单
python -m src.cli menu
```

### API 端点

#### 健康检查
- `GET /api/health` - 健康检查

#### 餐厅 API
- `GET /api/restaurants/` - 获取餐厅列表（支持筛选、分页、排序）
- `POST /api/restaurants/` - 创建餐厅
- `GET /api/restaurants/<shop_id>` - 获取单个餐厅详情
- `PUT /api/restaurants/<shop_id>` - 更新餐厅
- `DELETE /api/restaurants/<shop_id>` - 删除餐厅（软删除）
- `POST /api/restaurants/import` - 导入 CSV
- `POST /api/restaurants/batch` - 批量操作（删除、更新）
- `GET /api/restaurants/export/csv` - 导出 CSV
- `GET /api/restaurants/export/excel` - 导出 Excel

#### 模板 API
- `GET /api/templates/` - 获取模板列表
- `GET /api/templates/<id>` - 获取模板详情
- `PUT /api/templates/<id>` - 更新模板
- `DELETE /api/templates/<id>` - 删除模板

#### 报告 API
- `POST /api/reports/generate` - 生成报告
  - 请求体：`{ "template_id": 1, "params": {...}, "format": "markdown", "save": false }`
  - 返回：包含 `text`、`markdown`、`html` 三种格式的报告内容

#### 统计 API
- `GET /api/statistics/overall` - 总体统计
- `GET /api/statistics/categories` - 菜系统计
- `GET /api/statistics/districts` - 商圈统计
- `GET /api/statistics/price-distribution` - 价格分布
- `GET /api/statistics/star-levels` - 星级统计
- `GET /api/statistics/top-restaurants` - 热门餐厅
- `GET /api/statistics/dashboard` - 仪表板数据

## 项目结构

```
.
├── src/                      # Python 后端代码
│   ├── api/                  # Flask API 路由
│   │   └── routes/
│   │       ├── restaurants.py   # 餐厅 API
│   │       ├── templates.py     # 模板 API
│   │       ├── reports.py       # 报告 API
│   │       └── statistics.py    # 统计 API
│   ├── db/                   # 数据库访问层
│   │   ├── dao/              # 数据访问对象
│   │   │   ├── restaurant_dao.py
│   │   │   ├── template_dao.py
│   │   │   └── report_dao.py
│   │   ├── connection.py     # 数据库连接
│   │   └── schema.sql        # 数据库 schema
│   ├── services/             # 业务逻辑层
│   │   ├── restaurant_service.py  # 餐厅服务
│   │   ├── template_service.py    # 模板服务
│   │   ├── report_service.py      # 报告服务
│   │   ├── query_service.py       # 查询服务
│   │   ├── export_service.py      # 导出服务
│   │   └── statistics_service.py  # 统计服务
│   ├── utils/                # 工具函数
│   │   ├── validators.py     # 数据验证
│   │   ├── renderer.py       # 模板渲染
│   │   └── formatters.py     # 格式化工具
│   ├── templates_seed/       # 模板种子数据
│   │   └── data.py           # 模板数据
│   ├── cli.py                # CLI 命令行工具
│   └── app.py                # Flask 应用入口
├── frontend/                 # React 前端代码
│   ├── src/
│   │   ├── api/              # API 客户端
│   │   │   ├── restaurants.ts    # 餐厅 API
│   │   │   ├── templates.ts      # 模板 API
│   │   │   ├── reports.ts        # 报告 API
│   │   │   └── statistics.ts        # 统计 API
│   │   ├── components/        # React 组件
│   │   │   ├── RestaurantTable.tsx      # 餐厅表格
│   │   │   ├── RestaurantFilters.tsx    # 筛选组件
│   │   │   ├── RestaurantDetail.tsx     # 餐厅详情
│   │   │   ├── TemplateManagement.tsx   # 模板管理
│   │   │   ├── ReportGenerator.tsx      # 报告生成
│   │   │   ├── Dashboard.tsx            # 统计仪表板
│   │   │   ├── Navigation.tsx           # 导航组件
│   │   │   ├── Pagination.tsx           # 分页组件
│   │   │   ├── ThemeToggle.tsx          # 主题切换
│   │   │   └── ErrorBoundary.tsx        # 错误边界
│   │   ├── hooks/            # React Hooks
│   │   │   └── useRestaurants.ts        # 餐厅数据 Hook
│   │   ├── types/            # TypeScript 类型定义
│   │   │   └── index.ts
│   │   ├── App.tsx           # 主应用组件
│   │   ├── main.tsx          # 入口文件
│   │   └── styles.css        # 样式文件
│   └── vite.config.ts        # Vite 配置
└── requirements.txt          # Python 依赖
```

## 开发建议

1. **后端开发**
   - 使用 `python -m src.app` 启动开发服务器
   - 修改代码后会自动重载（debug=True）

2. **前端开发**
   - 使用 `npm run dev` 启动开发服务器
   - 支持热重载（HMR）

3. **API 测试**
   - 使用 Postman 或 curl 测试 API
   - 查看浏览器 Network 标签检查请求

4. **数据库管理**
   - 数据库文件: `src/gz_foodcms.db`
   - 使用 SQLite 浏览器查看数据

## 常见问题

### 问题：前端无法连接后端

**解决方案：**
1. 确认后端已启动在 8000 端口
2. 检查 `frontend/vite.config.ts` 中的代理配置
3. 查看浏览器控制台的错误信息

### 问题：导入 CSV 失败

**解决方案：**
1. 检查 CSV 文件路径
2. 确认 CSV 文件格式正确
3. 查看终端错误日志

### 问题：模板渲染失败

**解决方案：**
1. 确认模板已初始化（`init-db --seed`）
2. 检查模板参数是否完整
3. 查看后端日志错误信息

### 问题：导出功能失败

**解决方案：**
1. 确认已安装 `openpyxl` 和 `pandas`：`pip install openpyxl pandas`
2. 检查筛选条件是否正确
3. 查看后端日志错误信息

### 问题：统计数据为空

**解决方案：**
1. 确认数据库中有数据
2. 检查数据是否标记为 `is_active = 1`
3. 查看后端日志错误信息

### 问题：暗色模式不生效

**解决方案：**
1. 检查浏览器是否支持 CSS 变量
2. 清除浏览器缓存
3. 检查 localStorage 是否被禁用

## 新功能使用说明

### 数据导出

1. 在餐厅列表页面，使用筛选条件筛选数据
2. 点击"导出 CSV"或"导出 Excel"按钮
3. 系统将根据当前筛选条件导出数据

### 数据统计

1. 点击导航栏中的"数据统计"按钮
2. 查看各类统计数据和表格
3. 统计数据包括：
   - 总体统计（8 个关键指标）
   - 菜系分布（Top 10）
   - 商圈分布（Top 10）
   - 价格分布
   - 星级分布
   - 热门餐厅（Top 10）

### 餐厅详情

1. 在餐厅列表页面，点击餐厅名称或"查看详情"按钮
2. 查看餐厅详细信息
3. 可以编辑或删除餐厅

### 批量操作

1. 在餐厅列表页面，勾选需要操作的餐厅
2. 点击"批量删除"按钮
3. 确认操作

### 暗色模式

1. 点击页面右上角的主题切换按钮（🌙/☀️）
2. 主题设置会自动保存
3. 下次访问时会自动应用保存的主题

### 模板管理

1. 点击导航栏中的"模板管理"按钮
2. 在左侧模板列表中，点击要查看的模板
3. 在右侧查看模板详情（标题、关键词、格式、占位符、内容、示例输出等）
4. 点击"编辑"按钮可以编辑模板
5. 编辑完成后，点击"保存"按钮保存更改
6. 点击"取消"按钮取消编辑

### 报告生成

1. 点击导航栏中的"报告生成"按钮
2. 选择要使用的模板（从下拉列表中选择）
3. 根据模板要求设置参数：
   - 模板 1（星级分布分析）：无需参数
   - 模板 2（性价比推荐）：价格上限、推荐数量
   - 模板 3（冬季暖胃）：商圈
   - 模板 4（隐藏宝藏）：商圈
   - 模板 5（商圈美食速览）：商圈
   - 模板 6（外卖推荐）：商圈、最低评分
4. 选择输出格式（文本、Markdown、HTML）
5. 可选择是否保存报告到数据库
6. 点击"生成报告"按钮生成报告
7. 生成后可以：
   - 切换格式查看报告（文本、Markdown、HTML）
   - 复制报告内容
   - 下载报告文件

React 18：构建界面的库，关注组件与渲染性能。
TypeScript：给 JS 加静态类型，提高可靠性与维护性。
Vite：极速的开发服务器与打包工具