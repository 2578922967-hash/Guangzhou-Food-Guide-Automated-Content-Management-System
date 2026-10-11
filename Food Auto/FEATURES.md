# 功能扩展文档

## 新增功能列表

### 1. 数据导出功能 ✅
- **CSV 导出**：支持导出当前筛选条件下的餐厅数据为 CSV 格式
- **Excel 导出**：支持导出当前筛选条件下的餐厅数据为 Excel 格式（带格式）
- **位置**：
  - 后端：`src/services/export_service.py`
  - API：`GET /api/restaurants/export/csv`、`GET /api/restaurants/export/excel`
  - 前端：`frontend/src/api/restaurants.ts`

### 2. 数据统计功能 ✅
- **总体统计**：餐厅总数、分类数、商圈数、平均价格、平均评分等
- **菜系统计**：各菜系的餐厅数量、平均价格、平均评分
- **商圈统计**：各商圈的餐厅数量、平均价格、平均评分
- **价格分布**：价格区间分布统计
- **星级统计**：各星级的餐厅数量和平均评分
- **热门餐厅**：按评分、评论数等排序的热门餐厅
- **位置**：
  - 后端：`src/services/statistics_service.py`
  - API：`GET /api/statistics/*`
  - 前端：`frontend/src/api/statistics.ts`

### 3. 餐厅详情页面 ⏳
- **功能**：显示单个餐厅的详细信息
- **位置**：`frontend/src/components/RestaurantDetail.tsx`

### 4. 批量操作功能 ✅
- **批量删除**：支持批量删除选中的餐厅
- **批量更新**：支持批量更新选中餐厅的某些字段
- **位置**：
  - 后端：`POST /api/restaurants/batch`
  - 前端：`frontend/src/components/RestaurantTable.tsx`

### 5. 数据可视化仪表板 ⏳
- **功能**：显示数据统计图表
- **图表类型**：
  - 菜系分布饼图
  - 价格分布柱状图
  - 商圈分布柱状图
  - 星级分布饼图
  - 评分趋势折线图
- **位置**：`frontend/src/components/Dashboard.tsx`

### 6. 暗色模式 ⏳
- **功能**：支持暗色主题切换
- **位置**：`frontend/src/components/ThemeToggle.tsx`

## 使用说明

### 数据导出

1. 在餐厅列表页面，点击"导出"按钮
2. 选择导出格式（CSV 或 Excel）
3. 系统将根据当前筛选条件导出数据

### 数据统计

1. 访问统计仪表板页面
2. 查看各类统计数据和图表
3. 可以通过筛选条件查看特定数据

### 批量操作

1. 在餐厅列表页面，勾选需要操作的餐厅
2. 点击"批量操作"按钮
3. 选择操作类型（删除或更新）
4. 确认操作

## API 端点

### 导出 API

- `GET /api/restaurants/export/csv` - 导出 CSV
- `GET /api/restaurants/export/excel` - 导出 Excel

### 统计 API

- `GET /api/statistics/overall` - 总体统计
- `GET /api/statistics/categories` - 菜系统计
- `GET /api/statistics/districts` - 商圈统计
- `GET /api/statistics/price-distribution` - 价格分布
- `GET /api/statistics/star-levels` - 星级统计
- `GET /api/statistics/top-restaurants` - 热门餐厅
- `GET /api/statistics/dashboard` - 仪表板数据

### 餐厅 API

- `GET /api/restaurants/<shop_id>` - 获取单个餐厅
- `PUT /api/restaurants/<shop_id>` - 更新餐厅
- `DELETE /api/restaurants/<shop_id>` - 删除餐厅
- `POST /api/restaurants/batch` - 批量操作

## 依赖安装

### 后端依赖

```bash
pip install openpyxl pandas
```

### 前端依赖

```bash
cd frontend
npm install recharts  # 用于数据可视化
```

## 待实现功能

1. ✅ 数据导出（CSV、Excel）
2. ✅ 数据统计 API
3. ⏳ 数据可视化仪表板
4. ⏳ 餐厅详情页面
5. ⏳ 批量操作 UI
6. ⏳ 暗色模式

## 注意事项

1. 导出功能会导出所有符合筛选条件的数据，不受分页限制
2. 批量操作需要谨慎使用，建议先测试
3. 统计数据的计算可能需要一些时间，建议添加缓存
4. 数据可视化需要安装 `recharts` 库

