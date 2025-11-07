from APITEST import get, post, put, delete, run_test, print_info

# ---------- 1. 基础 GET + 单字段提取 ----------
uid, uname, city = run_test(
    "1. 获取 1 号用户",
    get("https://jsonplaceholder.typicode.com/users/1"),
    "id", "name", "address.city"
)

# ---------- 2. 字符串插值 URL ----------
run_test(
    "2. 用 uid 查询该用户帖子列表",
    get(f"https://jsonplaceholder.typicode.com/users/{uid}/posts")
)

# ---------- 3. POST 创建资源 + 提取值 ----------
new_post = run_test(
    "3. 新建帖子",
    post(
        "https://jsonplaceholder.typicode.com/posts",
        body=f'{{"title":"{uname} 的帖子","body":"由脚本创建","userId":{uid}}}'
    ),
    "id"
)

# ---------------- 4. PUT 修改----------------
run_test(
    "4. 修改刚才的帖子",
    put(
        f"https://jsonplaceholder.typicode.com/posts/1",
        body='{"id":%d,"title":"已更新","body":"新内容","userId":%d}' % (new_post, uid)
    )
)

# ---------------- 5. 自定义头 ----------------
run_test(
    "5. 带自定义头查询帖子详情",
    get(
        f"https://jsonplaceholder.typicode.com/posts/1",
        headers={"X-Source": "APITEST-demo"}
    )
)

# ---------- 6. DELETE 删除 ----------
run_test(
    "6. 删除帖子",
    delete(f"https://jsonplaceholder.typicode.com/posts/{new_post}")
)

# ---------- 7. 预期 404：资源不存在 ----------
run_test(
    "7. 再次查询应返回 404（预期失败）",
    get(f"https://jsonplaceholder.typicode.com/posts/{new_post}", should_fail=True)
)

# ---------- 8. 深路径 + 多字段同时提取 ----------
lat, lng = run_test(
    "8. 提取用户地址坐标",
    get("https://jsonplaceholder.typicode.com/users/1"),
    "address.geo.lat", "address.geo.lng"
)

# ---------- 9. 输出自定义键值对信息 ----------
print_info(
    "输出键值对信息",
    {
        "用户 ID": uid,
        "用户姓名": uname,
        "所在城市": city,
        "帖子 ID": new_post,
        "纬度": lat,
        "经度": lng
    }
)

print("\n🎉 所有步骤完成！")
