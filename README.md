# APITEST - 一个轻量级的API测试库

`APITEST` 是一个用于简化API接口测试的Python迷你库。它基于 `requests` 和 `rich` 库，为您的API测试提供美观、易读的终端输出。

## ✨ 功能特性

- **HTTP方法支持**: 支持 `GET`, `POST`, `PUT`, `DELETE` 等常用的HTTP请求方法。
- **美观的输出**: 使用 `rich` 库，将API响应以格式化的面板形式展示在终端，支持JSON高亮和自定义颜色主题。
- **状态码高亮**: 根据HTTP状态码（2xx, 4xx, 5xx）自动着色，让成功和失败的请求一目了然。
- **链式调用**: 通过 `extract` 参数，您可以从一个API响应中提取数据，并将其用于后续的API请求。支持点语法提取深层嵌套的JSON字段，例如 `user.address.city`。
- **失败断言**: `should_fail` 参数允许您定义预期失败的测试用例，当接口如预期般失败时，测试将被标记为成功。
- **灵活的头部支持**: 支持添加自定义HTTP头部，包括通过 `key` 参数快速设置 `Authorization` Bearer Token。
- **异常处理**: 内置了请求异常和JSON解析异常的处理逻辑，确保测试脚本的健壮性。

## 📦 安装依赖

建议使用**uv**安装。

```bash
git clone https://github.com/zyoung11/API-TEST.git
cd API-TEST
uv sync

#----------------------编写测试逻辑--------------------
# touch TEST.py  # 建议新建一个Python文件
# uv run TEST.py  # 运行测试脚本
```

## 🚀 快速上手

下面是一个简单的示例，展示了如何使用 `APITEST` 来测试API。

```python
# TEST.py
from APITEST import get, post, put, delete, run_test

# ---------- 1. 最基础的 GET：获取资源并提取字段 ----------
uid = run_test(
    "1. 取 1 号用户",
    get("https://jsonplaceholder.typicode.com/users/1", extract="id")
)
# 提取到的 uid 会用于后续请求

# ---------- 2. 字符串拼接 URL：把上一步提取的值传进去 ----------
run_test(
    "2. 用提取的 id 查该用户详情",
    get(f"https://jsonplaceholder.typicode.com/users/{uid}")
)

# ---------- 3. POST：带 JSON 体提交，再提取返回字段 ----------
new_post = run_test(
    "3. 新建一篇帖子",
    post(
        "https://jsonplaceholder.typicode.com/posts",
        body=f'{{"title":"foo","body":"bar","userId":{uid}}}',
        extract="id"  # 把服务端返回的新帖子 id 拿出来
    )
)

# ---------- 4. PUT：修改刚创建的帖子 ----------
run_test(
    "4. 修改刚才的帖子",
    put(
        f"https://jsonplaceholder.typicode.com/posts/{new_post}",
        body='{"id":%d,"title":"updated","body":"new body","userId":1}' % new_post
    )
)

# ---------- 5. DELETE：示范自定义请求头 ----------
run_test(
    "5. 带自定义头删除帖子",
    delete(
        f"https://jsonplaceholder.typicode.com/posts/{new_post}",
        headers={"X-Custom": "demo"}  # 任意自定义头
    )
)

# ---------- 6. 预期失败：当接口返回 404 时我们希望测试“通过” ----------
run_test(
    "6. 预期 404 的 GET",
    get("https://jsonplaceholder.typicode.com/posts/999999", should_fail=True)
)

# ---------- 7. 点语法提取：提取 user 的 address.city ----------
city = run_test(
    "7. 提取用户的城市",
    get("https://jsonplaceholder.typicode.com/users/1", extract="address.city")
)
```

## 📖 API参考

### `run_test(description, response)`

执行一个测试并打印结果。

- `description` (str): 对这个测试的描述，将作为标题显示在结果面板上。
- `response` (Tuple): 由 `get`, `post`, `put`, `delete` 函数返回的元组。


### `post(url, body, key, should_fail, extract, headers)`
### `get(url, key, should_fail, extract, headers)`
### `put(url, body, key, should_fail, extract, headers)`
### `delete(url, key, should_fail, extract, headers)`

这些函数用于发起HTTP请求，它们的参数相似：

- `url` (str): 请求的URL。
- `body` (Optional[str]): 请求体，通常是一个JSON字符串。仅 `post` 和 `put` 支持。
- `key` (Optional[str]): 用于认证的Bearer Token。如果提供，会自动添加到请求头的 `Authorization` 字段。
- `should_fail` (bool): 如果设置为 `True`，则预期此请求会失败（返回非2xx状态码）。如果请求真的失败了，测试结果为成功 (✅)，反之则为失败 (❌)。默认为 `False`。
- `extract` (Optional[str]): 一个字符串键，用于从JSON响应中提取对应的值。如果提取成功，`run_test` 函数会返回这个值。支持使用点语法（例如 `user.address.city`）来提取深层嵌套的JSON对象中的值。
- `headers` (Optional[Dict[str, str]]): 一个字典，包含了需要添加到请求中的自定义头部。


