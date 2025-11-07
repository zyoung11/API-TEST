import requests
import json
from typing import Optional, Any, Tuple, Dict
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich import box

def _get_status_color(status_code: int) -> str:
    if 200 <= status_code < 300:
        return "green"
    if 400 <= status_code < 500:
        return "yellow"
    if 500 <= status_code < 600:
        return "red"
    return "white"

def print_info(title: str, info: Dict[str, Any]):
    console = Console()

    table = Table(
        show_header=True,
        header_style="magenta", 
        box=box.ROUNDED,
        expand=True
    )
    table.add_column("Key", style="dim", width=20)
    table.add_column("Value")

    for k, v in info.items():
        table.add_row(str(k), str(v))

    console.print(Panel(table, title=title, border_style="green", expand=True))

def _deep_get(obj: Any, path: str) -> Any:
    keys = path.split(".")
    cur = obj
    for k in keys:
        if isinstance(cur, dict):
            cur = cur.get(k)
        elif isinstance(cur, list) and k.isdigit():
            cur = cur[int(k)]
        else:
            return None
        if cur is None:
            break
    return cur

def run_test(description: str, response: Tuple[str, Any, int, Optional[str]]) -> Any:
    console = Console()
    status, content, status_code, extract = response
    color = _get_status_color(status_code)

    title = f"""{description}: {status} [bold {color}]HTTP {status_code}[/bold {color}]"""

    display_content = content
    if extract is None and isinstance(content, dict) and 'buckets' in content:
        display_content = content['buckets']

    if isinstance(display_content, dict) or isinstance(display_content, list):
        json_str = json.dumps(display_content, indent=4, ensure_ascii=False)
        body = Syntax(json_str, "json", theme="dracula", line_numbers=True, background_color="default")
    else:
        body = str(display_content)

    console.print(
        Panel(
            body,
            title=title,
            border_style="blue",
            expand=True,
        )
    )
    console.print()

    if extract:
        value = _deep_get(content, extract)
        if value is not None:
            return value
        console.print(f"[bold red]Warning:[/bold red] Could not extract '{extract}' from response.")
    return None


def post(url: str, body: Optional[str] = None, key: Optional[str] = None,
         should_fail: bool = False, extract: Optional[str] = None, headers: Optional[Dict[str, str]] = None) -> Tuple[str, Any, int, Optional[str]]:
    request_headers = {"Content-Type": "application/json"}
    if headers:
        request_headers.update(headers)
    if key:
        request_headers["Authorization"] = f"Bearer {key}"
    kwargs = {"headers": request_headers, "timeout": 10}
    if body:
        kwargs["data"] = body
    try:
        resp = requests.post(url, **kwargs)
        status_code = resp.status_code
        if 200 <= status_code < 300:
            if should_fail:
                return "❌", f"期望失败但成功: {status_code}", status_code, extract
            else:
                try:
                    return "✅", resp.json(), status_code, extract
                except ValueError:
                    return "✅", {"response": resp.text}, status_code, extract
        else:
            if should_fail:
                return "✅", {"error": f"状态码异常: {status_code}"}, status_code, extract
            else:
                return "❌", f"状态码异常: {status_code}", status_code, extract
    except Exception as e:
        return ("❌" if not should_fail else "✅"), str(e), 999, extract


def delete(url: str, key: Optional[str] = None, should_fail: bool = False, extract: Optional[str] = None, headers: Optional[Dict[str, str]] = None) -> Tuple[str, Any, int, Optional[str]]:
    request_headers = {"Content-Type": "application/json"}
    if headers:
        request_headers.update(headers)
    if key:
        request_headers["Authorization"] = f"Bearer {key}"
    try:
        resp = requests.delete(url, headers=request_headers, timeout=10)
        status_code = resp.status_code
        if 200 <= status_code < 300:
            if should_fail:
                return "❌", f"期望失败但成功: {status_code}", status_code, extract
            else:
                try:
                    return "✅", resp.json(), status_code, extract
                except ValueError:
                    return "✅", {"response": resp.text}, status_code, extract
        else:
            if should_fail:
                return "✅", {"error": f"状态码异常: {status_code}"}, status_code, extract
            else:
                return "❌", f"状态码异常: {status_code}", status_code, extract
    except Exception as e:
        return ("❌" if not should_fail else "✅"), str(e), 999, extract


def put(url: str, body: Optional[str] = None, key: Optional[str] = None, should_fail: bool = False, extract: Optional[str] = None, headers: Optional[Dict[str, str]] = None) -> Tuple[str, Any, int, Optional[str]]:
    request_headers = {"Content-Type": "application/json"}
    if headers:
        request_headers.update(headers)
    if key:
        request_headers["Authorization"] = f"Bearer {key}"
    kwargs = {"headers": request_headers, "timeout": 10}
    if body:
        kwargs["data"] = body
    try:
        resp = requests.put(url, **kwargs)
        status_code = resp.status_code
        if 200 <= status_code < 300:
            if should_fail:
                return "❌", f"期望失败但成功: {status_code}", status_code, extract
            else:
                try:
                    return "✅", resp.json(), status_code, extract
                except ValueError:
                    return "✅", {"response": resp.text}, status_code, extract
        else:
            if should_fail:
                return "✅", {"error": f"状态码异常: {status_code}"}, status_code, extract
            else:
                return "❌", f"状态码异常: {status_code}", status_code, extract
    except Exception as e:
        return ("❌" if not should_fail else "✅"), str(e), 999, extract


def get(url: str, key: Optional[str] = None, should_fail: bool = False, extract: Optional[str] = None, headers: Optional[Dict[str, str]] = None) -> Tuple[str, Any, int, Optional[str]]:
    request_headers = {"Content-Type": "application/json"}
    if headers:
        request_headers.update(headers)
    if key:
        request_headers["Authorization"] = f"Bearer {key}"
    try:
        resp = requests.get(url, headers=request_headers, timeout=10)
        status_code = resp.status_code
        if not (200 <= status_code < 300):
            if should_fail:
                return "✅", f"状态码异常: {status_code}", status_code, extract
            else:
                return "❌", f"状态码异常: {status_code}", status_code, extract
        try:
            json_data = resp.json()
        except ValueError:
            return ("❌" if not should_fail else "✅"), "响应不是有效的JSON格式", status_code, extract

        if should_fail:
            return "❌", "期望失败但成功", status_code, extract
        else:
            return "✅", json_data, status_code, extract
    except Exception as e:
        return ("❌" if not should_fail else "✅"), str(e), 999, extract


