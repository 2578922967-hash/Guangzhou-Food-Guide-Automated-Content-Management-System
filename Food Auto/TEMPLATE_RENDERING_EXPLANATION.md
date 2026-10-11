# 模板渲染引擎技术说明

## 论文中提到的内容

论文中提到：
> 渲染引擎使用Python的string.Formatter类，带有自定义的StrictFormatter，强制执行占位符验证。这确保所有必需数据字段在渲染前都存在，防止不完整报告。格式化程序支持：
> - 命名占位符：{variable_name}
> - 格式说明符：{price:.1f}用于数字格式化
> - 复杂表达式：{avg_env_service_four_star:.1f}用于计算值

## 代码实现位置

### 1. StrictFormatter 类定义

**位置：** `src/utils/renderer.py` 第26-36行

```python
class StrictFormatter(Formatter):
    """
    对 str.format 进行包装，当占位符缺失时抛出异常。
    """
    
    def get_value(self, key, args, kwargs):
        if isinstance(key, str):
            if key in kwargs:
                return kwargs[key]
            raise MissingPlaceholderError(key)  # 如果占位符不存在，抛出异常
        return super().get_value(key, args, kwargs)
```

**作用说明：**
- 继承自Python标准库的 `string.Formatter` 类
- 重写了 `get_value` 方法，添加了严格的验证机制
- **关键点**：如果模板中有一个占位符（如 `{percentage_five_star}`），但在context数据字典中找不到对应的key，就会立即抛出 `MissingPlaceholderError` 异常
- 这确保了报告生成时不会出现 "未填充的占位符"，保证报告完整性

### 2. MissingPlaceholderError 异常类

**位置：** `src/utils/renderer.py` 第20-23行

```python
class MissingPlaceholderError(KeyError):
    """
    占位符缺失异常。
    """
```

**作用说明：**
- 自定义异常类，继承自 `KeyError`
- 当模板中有占位符但数据字典中没有对应值时，会抛出这个异常
- 在报告生成过程中被捕获，可以给用户明确的错误提示

### 3. render_text 函数 - 核心渲染函数

**位置：** `src/utils/renderer.py` 第39-41行

```python
def render_text(template: str, context: Mapping[str, Any]) -> str:
    formatter = StrictFormatter()  # 创建StrictFormatter实例
    return formatter.format(template, **context)  # 使用context数据填充模板
```

**调用位置：** `src/services/report_service.py` 第252行

```python
rendered_default = renderer.render_text(content, context)
```

**工作流程：**
1. 接收模板字符串（包含占位符）
2. 接收context字典（包含要填充的数据）
3. 使用 `StrictFormatter` 进行格式化
4. 如果所有占位符都能在context中找到，返回完整的报告
5. 如果有占位符缺失，抛出异常，阻止生成不完整的报告

## 三种占位符类型示例

### 类型1：命名占位符 - {variable_name}

**模板示例（模板1）：**
```markdown
"**Five-Star Merchant Percentage:** {percentage_five_star:.1f}%"
```

**对应代码：** `src/templates_seed/data.py` 第18行

**Context数据示例：**
```python
context = {
    "percentage_five_star": 32.3,
    # ... 其他数据
}
```

**渲染结果：**
```
**Five-Star Merchant Percentage:** 32.3%
```

### 类型2：格式说明符 - {price:.1f}

**模板示例（模板2）：**
```markdown
"**Avg Price:** ¥{restaurant1_price}"
```

**对应代码：** `src/templates_seed/data.py` 第99行

**说明：**
- `:.1f` 是Python字符串格式化的格式说明符
- `.1f` 表示保留1位小数的浮点数
- `{restaurant1_price:.1f}` 会将数字格式化为如 "80.0" 的形式

**Context数据：**
```python
context = {
    "restaurant1_price": 78.5,
    # ... 其他数据
}
```

**渲染结果：**
```
**Avg Price:** ¥78.5
```

### 类型3：复杂表达式 - {avg_env_service_four_star:.1f}

**模板示例（模板1）：**
```markdown
"Environment and service average score reaches **{avg_env_service_four_star:.1f}**"
```

**对应代码：** `src/templates_seed/data.py` 第34行

**说明：**
- `avg_env_service_four_star` 是一个计算出来的复合值
- 在SQL查询中计算：`AVG((environment_score + service_score) / 2.0)`
- 这个值在 `query_service.py` 中被计算并放入context

**对应的SQL查询：** `src/services/query_service.py` 第54行

```sql
AVG((environment_score + service_score) / 2.0) AS avg_env_service
```

**Context数据：**
```python
context = {
    "avg_env_service_four_star": 8.3,
    # ... 其他数据
}
```

**渲染结果：**
```
Environment and service average score reaches **8.3**
```

## 完整工作流程示例

### 步骤1：模板定义（Template 1）

**位置：** `src/templates_seed/data.py` 第13-42行

```python
"content": (
    "# Guangzhou Catering Star Rating Distribution Analysis\n"
    "**Five-Star Merchant Percentage:** {percentage_five_star:.1f}%\n"
    "**Taste:** {avg_taste_five:.1f}/10\n"
    # ... 更多占位符
)
```

### 步骤2：数据查询和Context构建

**位置：** `src/services/query_service.py` 第23-113行

```python
def star_rating_distribution() -> dict[str, Any]:
    # 执行SQL查询
    sql = """
    WITH filtered AS (...)
    SELECT ... FROM ...
    """
    # 查询结果转换为字典
    data = dict(row or {})
    
    # 计算百分比等派生值
    percentage_five_star = (five / total) * 100
    
    # 返回context字典
    return {
        "percentage_five_star": percentage_five_star,
        "avg_taste_five": data.get("avg_taste_five"),
        # ... 所有模板需要的占位符
    }
```

### 步骤3：模板渲染

**位置：** `src/services/report_service.py` 第250-252行

```python
def _render_outputs(template: dict[str, Any], context: dict[str, Any], template_id: int = None):
    content = template["content"]  # 获取模板内容
    # 调用render_text，使用StrictFormatter进行严格验证
    rendered_default = renderer.render_text(content, context)
```

**StrictFormatter的工作：**
1. 扫描模板中的所有占位符：`{percentage_five_star:.1f}`, `{avg_taste_five:.1f}`, 等
2. 检查每个占位符是否在context字典中存在
3. 如果全部存在，进行格式化替换
4. 如果任何占位符缺失，抛出 `MissingPlaceholderError`

### 步骤4：错误处理

**位置：** `src/services/report_service.py` 第296-302行

```python
try:
    outputs["title"] = renderer.render_text(title_template, context)
except renderer.MissingPlaceholderError:
    # 如果占位符缺失，使用原始模板作为标题
    outputs["title"] = title_template
```

## 实际运行示例

### 成功场景

**模板：**
```
"餐厅总数：{total_restaurants}"
```

**Context：**
```python
{"total_restaurants": 299}
```

**结果：**
```
餐厅总数：299
✅ 成功：占位符存在，正常替换
```

### 失败场景（演示StrictFormatter的作用）

**模板：**
```
"餐厅总数：{total_restaurants}"
```

**Context：**
```python
{"avg_price": 119.2}  # 缺少 total_restaurants
```

**结果：**
```
❌ MissingPlaceholderError: 'total_restaurants'
✅ 好处：立即发现数据不完整，不会生成有空白占位符的错误报告
```

## 与传统format的区别

### Python标准 format() 方法

```python
template = "价格：{price}"
context = {"price": 100}
result = template.format(**context)  # ✅ 工作正常

template = "价格：{price}"
context = {}  # 缺少price
result = template.format(**context)  # ❌ KeyError，但没有明确的错误信息
```

### 我们的 StrictFormatter

```python
template = "价格：{price}"
context = {}
formatter = StrictFormatter()
result = formatter.format(template, **context)  
# ❌ 抛出 MissingPlaceholderError('price')
# ✅ 明确的错误信息，知道是哪个占位符缺失
```

## 总结

1. **StrictFormatter位置**：`src/utils/renderer.py` 第26-36行
2. **使用位置**：`src/utils/renderer.py` 的 `render_text()` 函数（第39-41行）
3. **调用位置**：`src/services/report_service.py` 第252行
4. **模板示例**：`src/templates_seed/data.py` 中所有模板的 `content` 字段
5. **数据来源**：`src/services/query_service.py` 中各个查询函数返回的字典

整个系统的核心就是：**模板定义占位符 → SQL查询提供数据 → StrictFormatter严格验证 → 生成完整报告**

