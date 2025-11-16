from PAT import get, option, patch, post, put, delete, run_test, print_info

# ---------- 1. 基础 GET + 多字段提取 ----------
uid, uname, city = run_test(
    "1. 获取 1 号用户",
    get("https://jsonplaceholder.typicode.com/users/1"),
    "id",
    "name",
    "address.city"
)

# ---------- 2. 字符串插值 URL ----------
run_test(
    "2. 用 uid 查询该用户帖子列表",
    get(f"https://jsonplaceholder.typicode.com/users/{uid}/posts")
)

# ---------- 3. 获取单个列表元素字段 ----------
body, title = run_test(
    "3. 用 uid 查询该用户帖子列表",
    get(f"https://jsonplaceholder.typicode.com/users/{uid}/posts"),
    "0.body",
    "0.title"
)

# ---------- 4. POST 创建资源 + 提取值 ----------
new_post = run_test(
    "4. 新建帖子",
    post(
        "https://jsonplaceholder.typicode.com/posts",
        body={
            "title":"帖子",
            "body":"由脚本创建",
            "userId":uid
        }
    ),
    "id"
)

# ---------------- 5. PUT 修改----------------
run_test(
    "5. 修改刚才的帖子",
    put(
        "https://jsonplaceholder.typicode.com/posts/1",
        body={
            "id":new_post,
            "title":"已更新",
            "body":"新内容",
            "userId":uid
        }
    )
)

# ---------------- 6. PATCH 修改----------------
run_test(
    "6. 修改刚才的帖子",
    patch(
        "https://jsonplaceholder.typicode.com/posts/1",
        body={
            "id":new_post,
            "title":"已更新",
            "body":"新内容",
            "userId":uid
        }
    )
)


# ---------------- 7. 自定义头 ----------------
run_test(
    "7. 带自定义头查询帖子详情",
    get(
        "https://jsonplaceholder.typicode.com/posts/1",
        headers={"X-Source": "APITEST-demo"}
    )
)

# ---------------- 8. OPTION ----------------
run_test(
    "8. 带自定义头查询帖子详情",
    option(
        "https://jsonplaceholder.typicode.com/posts/1"
    )
)

# ---------- 9. DELETE 删除 ----------
run_test(
    "9. 删除帖子",
    delete(f"https://jsonplaceholder.typicode.com/posts/{new_post}")
)

# ---------- 10. 预期 404：资源不存在 ----------
run_test(
    "10. 再次查询应返回 404（预期失败）",
    get(f"https://jsonplaceholder.typicode.com/posts/{new_post}", should_fail=True)
)

# ---------- 11. 深路径 + 多字段同时提取 ----------
lat, lng = run_test(
    "11. 提取用户地址坐标",
    get("https://jsonplaceholder.typicode.com/users/1"),
    "address.geo.lat", "address.geo.lng"
)

# ---------- 12. 输出自定义键值对信息 ----------
print_info(
    "输出键值对信息",
    {
        "用户 ID": uid,
        "用户姓名": uname,
        "所在城市": city,
        "帖子 ID": new_post,
        "用户的文章标题": title,
        "用户的文章内容": body,
        "纬度": lat,
        "经度": lng
    }
)

print("\n🎉 所有步骤完成！")
