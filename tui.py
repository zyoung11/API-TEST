# APITEST_TUI.py  单文件完整版
from __future__ import annotations
import requests
import json
import queue
import threading
import time
from typing import Optional, Any, Tuple, Dict
# ---------------- Rich 相关 ----------------
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich import box
from rich.layout import Layout
from rich.live import Live
from rich.align import Align
from rich.text import Text

# ------------------------------------------------------------------
# 1. 全局队列：生产（run_test/print_info） -> 消费（TUI 刷新）
# ------------------------------------------------------------------
_LOG_Q: queue.Queue[Panel] = queue.Queue()
_INFO_Q: queue.Queue[Table] = queue.Queue()

# ------------------------------------------------------------------
# 2. TUI 布局：大筐分 header / body(左日志+右详情) / footer
# ------------------------------------------------------------------
def _make_layout() -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=1)
    )
    layout["body"].split_row(
        Layout(name="log", ratio=2),
        Layout(name="info", ratio=1)
    )
    # 顶部 banner
    title_text = Text("API 集成测试面板", style="bold cyan", justify="center")
    layout["header"].update(Panel(Align.center(title_text), border_style="cyan"))
    layout["footer"].update(Text("按 Ctrl+C 退出", style="dim"))
    return layout

_LAYOUT = _make_layout()

# ------------------------------------------------------------------
# 3. 消费者：在 Live 周期内不断读队列刷新界面
# ------------------------------------------------------------------
def _ui_worker(stop_evt: threading.Event):
    log_panel = Panel("等待日志...", title="运行日志", border_style="bright_black")
    info_table = Table(title="信息汇总", box=box.ROUNDED, show_header=True, header_style="magenta")
    info_table.add_column("Key", style="dim", width=20)
    info_table.add_column("Value")
    while not stop_evt.is_set():
        try:
            log_panel = _LOG_Q.get_nowait()
        except queue.Empty:
            pass
        try:
            info_table = _INFO_Q.get_nowait()
        except queue.Empty:
            pass

        _LAYOUT["log"].update(log_panel)
        _LAYOUT["info"].update(Panel(info_table, title="信息汇总", border_style="green"))
        time.sleep(0.02)   # 50 FPS 足够流畅

# ------------------------------------------------------------------
# 4. 工具函数：颜色 / deep_get / HTTP 请求
# ------------------------------------------------------------------
def _get_status_color(code: int) -> str:
    if 200 <= code < 300:
        return "green"
    if 400 <= code < 500:
        return "yellow"
    if 500 <= code < 600:
        return "red"
    return "white"

def _deep_get(obj: Any, path: str) -> Any:
    cur = obj
    for k in path.split("."):
        if isinstance(cur, dict):
            cur = cur.get(k)
        elif isinstance(cur, list) and k.isdigit():
            cur = cur[int(k)]
        else:
            return None
        if cur is None:
            break
    return cur

# HTTP 动词封装（返回格式同原来）
def post(url: str, body: Optional[str] = None, key: Optional[str] = None,
         should_fail: bool = False, extract: Optional[str] = None, headers: Optional[Dict[str, str]] = None
         ) -> Tuple[str, Any, int, Optional[str]]:
    h = {"Content-Type": "application/json"}
    if headers:
        h.update(headers)
    if key:
        h["Authorization"] = f"Bearer {key}"
    kwargs = {"headers": h, "timeout": 10}
    if body:
        kwargs["data"] = body
    try:
        r = requests.post(url, **kwargs)
        sc = r.status_code
        if 200 <= sc < 300:
            if should_fail:
                return "❌", f"期望失败但成功: {sc}", sc, extract
            try:
                return "✅", r.json(), sc, extract
            except ValueError:
                return "✅", {"response": r.text}, sc, extract
        else:
            if should_fail:
                return "✅", {"error": f"状态码异常: {sc}"}, sc, extract
            return "❌", f"状态码异常: {sc}", sc, extract
    except Exception as e:
        return ("❌" if not should_fail else "✅"), str(e), 999, extract

def delete(url: str, key: Optional[str] = None, should_fail: bool = False,
           extract: Optional[str] = None, headers: Optional[Dict[str, str]] = None
           ) -> Tuple[str, Any, int, Optional[str]]:
    h = {"Content-Type": "application/json"}
    if headers:
        h.update(headers)
    if key:
        h["Authorization"] = f"Bearer {key}"
    try:
        r = requests.delete(url, headers=h, timeout=10)
        sc = r.status_code
        if 200 <= sc < 300:
            if should_fail:
                return "❌", f"期望失败但成功: {sc}", sc, extract
            try:
                return "✅", r.json(), sc, extract
            except ValueError:
                return "✅", {"response": r.text}, sc, extract
        else:
            if should_fail:
                return "✅", {"error": f"状态码异常: {sc}"}, sc, extract
            return "❌", f"状态码异常: {sc}", sc, extract
    except Exception as e:
        return ("❌" if not should_fail else "✅"), str(e), 999, extract

def put(url: str, body: Optional[str] = None, key: Optional[str] = None,
        should_fail: bool = False, extract: Optional[str] = None, headers: Optional[Dict[str, str]] = None
        ) -> Tuple[str, Any, int, Optional[str]]:
    h = {"Content-Type": "application/json"}
    if headers:
        h.update(headers)
    if key:
        h["Authorization"] = f"Bearer {key}"
    kwargs = {"headers": h, "timeout": 10}
    if body:
        kwargs["data"] = body
    try:
        r = requests.put(url, **kwargs)
        sc = r.status_code
        if 200 <= sc < 300:
            if should_fail:
                return "❌", f"期望失败但成功: {sc}", sc, extract
            try:
                return "✅", r.json(), sc, extract
            except ValueError:
                return "✅", {"response": r.text}, sc, extract
        else:
            if should_fail:
                return "✅", {"error": f"状态码异常: {sc}"}, sc, extract
            return "❌", f"状态码异常: {sc}", sc, extract
    except Exception as e:
        return ("❌" if not should_fail else "✅"), str(e), 999, extract

def get(url: str, key: Optional[str] = None, should_fail: bool = False,
        extract: Optional[str] = None, headers: Optional[Dict[str, str]] = None
        ) -> Tuple[str, Any, int, Optional[str]]:
    h = {"Content-Type": "application/json"}
    if headers:
        h.update(headers)
    if key:
        h["Authorization"] = f"Bearer {key}"
    try:
        r = requests.get(url, headers=h, timeout=10)
        sc = r.status_code
        if not (200 <= sc < 300):
            if should_fail:
                return "✅", f"状态码异常: {sc}", sc, extract
            return "❌", f"状态码异常: {sc}", sc, extract
        try:
            data = r.json()
        except ValueError:
            return ("❌" if not should_fail else "✅"), "响应不是有效的JSON格式", sc, extract
        if should_fail:
            return "❌", "期望失败但成功", sc, extract
        return "✅", data, sc, extract
    except Exception as e:
        return ("❌" if not should_fail else "✅"), str(e), 999, extract

# ------------------------------------------------------------------
# 5. run_test & print_info  只把对象送进队列，不直接打印
# ------------------------------------------------------------------
def run_test(description: str, response: Tuple[str, Any, int, Optional[str]]) -> Any:
    status, content, status_code, extract = response
    color = _get_status_color(status_code)
    title = f"{description}: {status} [bold {_get_status_color(status_code)}]HTTP {status_code}[/]"

    display = content
    if extract is None and isinstance(content, dict) and 'buckets' in content:
        display = content['buckets']

    if isinstance(display, (dict, list)):
        body = Syntax(json.dumps(display, indent=4, ensure_ascii=False),
                      "json", theme="dracula", line_numbers=True, background_color="default")
    else:
        body = str(display)

    panel = Panel(body, title=title, border_style="blue", expand=True)
    _LOG_Q.put(panel)          # ← 送进队列，由 TUI 刷新

    if extract:
        val = _deep_get(content, extract)
        if val is not None:
            return val
        # 警告也塞进日志
        _LOG_Q.put(Panel(f"[bold red]Warning:[/] 提取 '{extract}' 失败", border_style="red"))
    return None

def print_info(title: str, info: Dict[str, Any]):
    table = Table(title=title, box=box.ROUNDED, expand=True, header_style="magenta")
    table.add_column("Key", style="dim", width=20)
    table.add_column("Value")
    for k, v in info.items():
        table.add_row(str(k), str(v))
    _INFO_Q.put(table)           # ← 送进队列

# ------------------------------------------------------------------
# 6. 你的测试代码原封不动
# ------------------------------------------------------------------
if __name__ == "__main__":
    stop_evt = threading.Event()
    # 启动 TUI 消费者线程
    ui_thread = threading.Thread(target=_ui_worker, args=(stop_evt,), daemon=True)
    ui_thread.start()

    try:
        with Live(_LAYOUT, refresh_per_second=20, screen=True):
            # ---------- 1. 最基础的 GET ----------
            uid = run_test(
                "1. 取 1 号用户",
                get("https://jsonplaceholder.typicode.com/users/1", extract="id")
            )

            # ---------- 2. 字符串拼接 URL ----------
            run_test(
                "2. 用提取的 id 查该用户详情",
                get(f"https://jsonplaceholder.typicode.com/users/{uid}")
            )

            # ---------- 3. POST ----------
            new_post = run_test(
                "3. 新建一篇帖子",
                post("https://jsonplaceholder.typicode.com/posts",
                     body=f'{{"title":"foo","body":"bar","userId":{uid}}}', extract="id")
            )

            # ---------- 4. PUT ----------
            run_test(
                "4. 修改刚才的帖子",
                put(f"https://jsonplaceholder.typicode.com/posts/{new_post}",
                    body='{"id":%d,"title":"updated","body":"new body","userId":1}' % new_post)
            )

            # ---------- 5. DELETE ----------
            run_test(
                "5. 带自定义头删除帖子",
                delete(f"https://jsonplaceholder.typicode.com/posts/{new_post}",
                       headers={"X-Custom": "demo"})
            )

            # ---------- 6. 预期失败 ----------
            run_test(
                "6. 预期 404 的 GET",
                get("https://jsonplaceholder.typicode.com/posts/999999", should_fail=True)
            )

            # ---------- 7. 点语法提取 ----------
            city = run_test(
                "7. 提取用户的城市",
                get("https://jsonplaceholder.typicode.com/users/1", extract="address.city")
            )

            # ---------- 8. print_info ----------
            print_info("用户信息", {"用户ID": uid, "城市": city, "新帖子ID": new_post})

            # 所有测试已在后台启动, TUI 会持续刷新
            # 主线程在此循环以保持程序运行, 直到用户按下 Ctrl+C
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        # 收到退出信号
        pass
    finally:
        # 通知 UI 线程停止
        stop_evt.set()
