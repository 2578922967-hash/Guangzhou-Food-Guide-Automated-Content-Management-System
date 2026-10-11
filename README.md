# 广州美食指南自动化内容管理系统

本仓库为 `AIDM7360` 课程小组项目提交仓库，包含系统源码、报告与答辩材料。

## 仓库内容

- `Food Auto/`：完整项目代码（后端、前端、数据库与模板）
- `Report.pdf`：项目最终报告
- `副本Guangzhou Food Guide Automated Content Management System.pptx`：项目汇报演示文稿

## 项目背景与目标

本项目聚焦“广州美食指南”的内容管理与自动化报告生成场景，核心目标包括：

1. 统一管理餐厅数据（评分、价格、商圈、推荐菜等）
2. 基于模板和数据库查询自动生成美食报告
3. 支持多格式输出（Text / Markdown / HTML）
4. 通过聚合函数与子查询实现更深入的数据分析

系统面向 299+ 条餐厅数据，覆盖星级、菜系、商圈、口味/环境/服务等多维度字段。

## 系统架构

项目采用三层架构：

- 数据层：`SQLite`
- 后端层：`Flask RESTful API`（DAO + Service 分层）
- 前端层：`React + TypeScript + Vite`

## 主要功能

- 餐厅数据管理：增删改查、筛选、排序、分页、详情查看
- 模板管理：模板查看、编辑、版本化管理
- 报告生成：按模板动态生成内容，可选择输出格式并下载/保存
- 数据统计：总体统计、菜系分布、商圈分布、价格分布、星级分布、热门餐厅
- 批量与导出：批量操作、CSV/Excel 导出

## 查询与模板能力（来自报告）

系统在查询层使用了多类 SQL 能力：

- 聚合函数：`COUNT`、`AVG`、`MAX`、`MIN`、`SUM`
- 子查询：相关子查询、标量子查询、`EXISTS`
- CTE：用于多阶段统计分析

预置 6 类报告模板，包括：

1. 星级分布与评分表现
2. 性价比推荐
3. 冬季暖胃推荐
4. 隐藏宝藏餐厅发现
5. 商圈美食速览
6. 外卖友好型餐厅推荐

## 项目结果与发现（来自 `Report.pdf`）

- 数据规模：成功管理 299 条活跃餐厅记录
- 模板能力：内置 6 个高频分析模板
- 查询性能：复杂聚合查询在合理索引下可达 `<50ms`
- 接口性能：分页列表接口平均响应约 `30-80ms`

项目在以下方面表现良好：

- 可扩展性：模板与查询类型易于扩展
- 数据完整性：外键约束 + 软删除机制
- 业务灵活性：模板化报告无需改代码即可生成多类内容
- 用户体验：支持实时筛选/排序、导出、主题切换与错误兜底

## 快速启动（`Food Auto`）

### 1) 启动后端

```bash
cd "Food Auto"
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.cli init-db --seed
python -m src.app
```

后端地址：`http://localhost:8000`

### 2) 启动前端

```bash
cd "Food Auto/frontend"
npm install
npm run dev
```

前端地址：`http://localhost:5173`

## 说明

- 本仓库用于课程项目提交与展示。
- 更细的功能说明与接口细节可参考 `Food Auto/README.md` 与 `Report.pdf`。
