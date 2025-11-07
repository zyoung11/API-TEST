# PAT - API 测试框架

## 概述

PAT 是一个基于 Python 的 API 测试框架，提供了简洁的语法和丰富的功能来编写和执行 HTTP API 测试。该框架支持所有主要的 HTTP 方法（GET、POST、PUT、PATCH、DELETE、OPTIONS），并内置了响应数据提取、断言验证和美观的结果展示功能。

## 功能特性

- 支持完整的 HTTP 方法：GET、POST、PUT、PATCH、DELETE、OPTIONS
- 链式 API 调用，支持响应数据提取并在后续测试中使用
- 深路径数据提取，支持嵌套 JSON 字段访问
- 自动化的成功/失败断言
- 丰富的终端输出，使用 Rich 库提供美观的格式化显示
- 自定义请求头支持
- 错误处理和异常捕获
- 简洁的 API 设计，易于编写和维护测试用例

## 安装

推荐使用 uv 包管理器进行安装：

> 下载uv: https://docs.astral.sh/uv/getting-started/installation

```bash
git clone https://github.com/zyoung11/API-TEST.git

# 创建项目目录
mkdir API-TEST
cd API-TEST

# 创建虚拟环境并安装依赖
uv sync
```

## 基本用法

### 1. 创建测试文件

创建一个新的 Python 文件（例如 `my_test.py`），导入必要的模块：

```python
from PAT import get, post, put, patch, delete, option, run_test, print_info
```

### 2. 基础 GET 请求与数据提取

```python
# 发送 GET 请求并提取多个字段
user_id, user_name, city = run_test(
    "获取用户信息",
    get("https://jsonplaceholder.typicode.com/users/1"),
    "id", "name", "address.city"
)
```

### 3. 使用提取的数据进行链式调用

```python
# 使用之前提取的 user_id 构建 URL
run_test(
    "查询用户帖子列表",
    get(f"https://jsonplaceholder.typicode.com/users/{user_id}/posts")
)
```

### 4. POST 请求创建资源

```python
# 创建新资源并提取返回的 ID
new_post_id = run_test(
    "创建新帖子",
    post(
        "https://jsonplaceholder.typicode.com/posts",
        body={
            "title": "测试帖子",
            "body": "这是通过 PAT 创建的帖子",
            "userId": user_id
        }
    ),
    "id"  # 提取响应中的 id 字段
)
```

### 5. PUT 和 PATCH 请求更新资源

```python
# 使用 PUT 完全更新资源
run_test(
    "更新帖子内容",
    put(
        "https://jsonplaceholder.typicode.com/posts/1",
        body={
            "id": new_post_id,
            "title": "更新后的标题",
            "body": "更新后的内容",
            "userId": user_id
        }
    )
)

# 使用 PATCH 部分更新资源
run_test(
    "部分更新帖子",
    patch(
        "https://jsonplaceholder.typicode.com/posts/1",
        body={
            "title": "仅更新标题"
        }
    )
)
```

### 6. DELETE 请求删除资源

```python
# 删除资源
run_test(
    "删除帖子",
    delete(f"https://jsonplaceholder.typicode.com/posts/{new_post_id}")
)
```

### 7. OPTIONS 请求

```python
# 查询资源支持的 HTTP 方法
run_test(
    "查询帖子支持的选项",
    option("https://jsonplaceholder.typicode.com/posts/1")
)
```

### 8. 自定义请求头

```python
# 添加自定义请求头
run_test(
    "带认证头的请求",
    get(
        "https://api.example.com/protected",
        headers={"Authorization": "Bearer your-token", "X-Custom-Header": "value"}
    )
)
```

### 9. 预期失败测试

```python
# 测试预期会失败的请求（如删除不存在的资源）
run_test(
    "验证资源不存在",
    get(f"https://jsonplaceholder.typicode.com/posts/{new_post_id}", should_fail=True)
)
```

### 10. 深路径数据提取

```python
# 提取嵌套的 JSON 数据
latitude, longitude = run_test(
    "提取用户地理坐标",
    get("https://jsonplaceholder.typicode.com/users/1"),
    "address.geo.lat", "address.geo.lng"
)
```

### 11. 输出测试信息

```python
# 在测试结束时输出汇总信息
print_info(
    "测试结果汇总",
    {
        "用户ID": user_id,
        "用户名": user_name,
        "所在城市": city,
        "创建的帖子ID": new_post_id,
        "纬度": latitude,
        "经度": longitude
    }
)
```

## 函数参考

### HTTP 方法函数

所有 HTTP 方法函数都支持以下参数：

- •`url`: 请求的 URL
- •`body`: 请求体（对于 POST、PUT、PATCH）
- •`headers`: 自定义请求头
- •`should_fail`: 布尔值，表示是否期望请求失败

### run_test 函数

```python
run_test(description, response, *extract_paths)
```

- •`description`: 测试描述，显示在输出中
- •`response`: HTTP 方法函数返回的响应元组
- •`extract_paths`: 可变参数，指定要从响应中提取的字段路径

### print_info 函数

```python
print_info(title, info_dict)
```

- •`title`: 信息面板的标题
- •`info_dict`: 要显示的键值对字典

## 响应数据提取语法

使用点号表示法访问嵌套的 JSON 字段：

- •`"id"` - 提取顶层的 id 字段
- •`"address.city"` - 提取 address 对象中的 city 字段
- •`"address.geo.lat"` - 提取嵌套的经纬度信息

## 错误处理

框架会自动处理以下情况：

- •非 2xx 状态码（除非使用 `should_fail=True`）
- •JSON 解析错误
- •网络连接异常
- •数据提取路径不存在

## 运行测试

保存测试文件后，直接运行：

```bash
uv run my_test.py
```

框架会自动执行所有测试步骤，并在终端中显示格式化的结果。

## 最佳实践

1. **清晰的描述**: 为每个测试步骤提供有意义的描述
2. **错误处理**: 合理使用 `should_fail` 参数来验证错误场景
3. **结果验证**: 使用 `print_info` 输出关键测试数据用于验证
