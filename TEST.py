# TEST.py
from APITEST import get, post, put, delete, run_test, print_info

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

# ---------- 8. 使用 print_info 打印信息 ----------
print_info(
    "用户信息",
    {
        "用户ID": uid,
        "城市": city,
        "新帖子ID": new_post
    }
)

