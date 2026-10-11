# 数据清理分析报告

## 当前状态

### 数据文件格式
- **实际文件**：`src/data/GuangZhou_food.csv`（CSV格式）
- **数据量**：299条餐厅记录
- **Excel支持**：系统目前**只支持CSV导入**，虽然有Excel导出功能，但**不支持Excel导入**

### 数据清理机制

系统在导入数据时确实进行了清理，主要通过 `src/utils/validators.py` 中的 `normalize_restaurant_record()` 函数实现。

## 数据清理的具体步骤

### 1. 字段名称映射（Field Aliasing）
**位置**：`src/utils/validators.py` 第9-34行

```python
CSV_FIELD_ALIASES = {
    "Name": "name",
    "Restaurant Name": "name",
    "Reviews": "reviews",
    "Avg price (RMB)": "avg_price",
    "Category": "category",
    "Cuisine Type": "category",
    # ... 更多映射
}
```

**作用**：统一不同的列名变体，例如：
- `"Name"` 和 `"Restaurant Name"` 都映射到 `"name"`
- `"Avg price (RMB)"` 映射到 `"avg_price"`
- `"Shop ID"` 和 `"ShopId"` 都映射到 `"shop_id"`

### 2. 字符串空白清理
**位置**：`src/utils/validators.py` 第99行

```python
trimmed = {key: (value.strip() if isinstance(value, str) else value) 
           for key, value in mapped.items()}
```

**作用**：去除所有字符串字段的前后空白字符（空格、制表符等）

### 3. 数据类型转换和验证
**位置**：`src/utils/validators.py` 第106-114行

#### 字符串字段处理
- 只保留非空字符串值
- 空字符串会被忽略（不写入数据库）

#### 浮点数字段处理
```python
FLOAT_FIELDS = {
    "avg_price",
    "taste_score",
    "environment_score",
    "service_score",
}
```
- 使用 `_coerce_float()` 函数进行转换
- 空值或无效值转换为 `None`
- 无效数值会抛出 `ValueError` 异常

#### 整数字段处理
```python
INT_FIELDS = {"reviews"}
```
- 使用 `_coerce_int()` 函数进行转换
- 空值或无效值转换为 `None`
- 支持从浮点数转换（如 2672.0 → 2672）

### 4. 必填字段验证
**位置**：`src/utils/validators.py` 第101-104行

```python
REQUIRED_RESTAURANT_FIELDS = {
    "shop_id",
    "name",
    "category",
    "star_level",
}
```

**作用**：
- 检查必填字段是否存在
- 如果缺失，抛出 `ValueError` 异常，阻止导入

### 5. 默认值设置
**位置**：`src/utils/validators.py` 第116-117行

```python
record.setdefault("reviews", 0)      # 如果没有评论数，默认为0
record.setdefault("is_active", 1)    # 默认激活状态为1（启用）
```

## 实际数据检查结果

从CSV文件分析：
- ✅ **无缺失值**：所有299条记录的15个字段都有值
- ✅ **数据类型正确**：数字字段为数值类型，文本字段为字符串
- ✅ **格式统一**：列名符合预期的映射规则

## 数据清理的局限性

### 1. 数据质量问题（需要额外清理）

#### a. Shop ID格式不一致
- 有些是纯数字：`66250176`
- 有些带"id"前缀：`id58456220`, `id110266597`, `id520094`

**影响**：可能导致查询和匹配问题

#### b. Star Level格式可能不一致
- `"Five-star merchant"` vs `"Five-Star Merchant"`
- 系统通过 `LOWER(star_level) LIKE 'five%'` 处理，但可能需要统一

#### c. 地址格式
- 包含引号和特殊字符
- 可能需要标准化处理

#### d. URL格式
- 所有URL都是有效的HTTP链接，但格式统一

### 2. 缺少的清理功能

#### a. 数据去重
- 目前没有检查重复的餐厅（基于shop_id）
- 依赖数据库的UNIQUE约束

#### b. 异常值检测
- 没有检测明显异常的数值（如价格为负数、评分超过10等）

#### c. 数据标准化
- Star Level可能需要统一格式（如统一大小写）
- Business District可能需要标准化拼写

#### d. 数据完整性检查
- 没有检查相关字段的逻辑关系（如评分应该在一定范围内）

## 建议改进的数据清理功能

### 1. Shop ID标准化
```python
def normalize_shop_id(shop_id: str) -> str:
    """统一Shop ID格式：移除'id'前缀，统一为纯数字字符串"""
    if shop_id.startswith('id'):
        return shop_id[2:]
    return shop_id
```

### 2. Star Level标准化
```python
def normalize_star_level(star_level: str) -> str:
    """统一星级格式：首字母大写，其余小写"""
    # "Five-star merchant" -> "Five-Star Merchant"
    # "Quasi five-star merchant" -> "Quasi-Five-Star Merchant"
```

### 3. 数值范围验证
```python
def validate_scores(taste, env, service):
    """验证评分在0-10范围内"""
    for score, name in [(taste, "taste"), (env, "environment"), (service, "service")]:
        if score is not None and (score < 0 or score > 10):
            raise ValueError(f"{name} score out of range: {score}")
```

### 4. 地址清理
```python
def clean_address(address: str) -> str:
    """清理地址中的引号和多余空格"""
    address = address.strip().strip('"').strip("'")
    address = re.sub(r'\s+', ' ', address)  # 多个空格合并为一个
    return address
```

## 总结

### 已实现的清理
✅ 字段名称映射和统一  
✅ 字符串空白去除  
✅ 数据类型转换  
✅ 必填字段验证  
✅ 默认值设置  

### 需要改进的清理
⚠️ Shop ID格式标准化  
⚠️ Star Level格式统一  
⚠️ 地址格式清理  
⚠️ 异常值检测  
⚠️ 数据去重检查  

### Excel导入功能
❌ **当前不支持Excel导入**，只支持CSV  
💡 **建议**：添加Excel导入功能，可以复用现有的数据清理逻辑

## 当前数据质量评估

- **数据完整性**：✅ 优秀（无缺失值）
- **数据格式**：⚠️ 良好（有轻微不一致）
- **数据准确性**：✅ 良好（数值在合理范围内）
- **数据一致性**：⚠️ 需要改进（Shop ID和Star Level格式不统一）

总体而言，数据已经过基本的清理和验证，但在格式标准化方面还有改进空间。

