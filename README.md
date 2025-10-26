# API-TEST

A mini Python library for API testing.

## Description

This library provides a simple way to test APIs with functions for `POST`, `GET`, `PUT`, and `DELETE` requests. It also has a `run_test` function to display the results in a formatted way using the `rich` library.

## Features

- Send `POST`, `GET`, `PUT`, and `DELETE` requests.
- Display formatted test results in the console.
- Extract data from the response body.
- Check for expected failures.

## Dependencies

- `requests`
- `rich`

You can install them using pip:

```bash
pip install requests rich
```

## Usage

### `post(url: str, body: Optional[str] = None, key: Optional[str] = None, should_fail: bool = False) -> Tuple[str, Any, int]`

Sends a POST request to the specified URL.

- `url`: The URL to send the request to.
- `body`: The request body.
- `key`: The authorization key.
- `should_fail`: If `True`, the test will pass if the request fails.

### `get(url: str, key: Optional[str] = None, should_fail: bool = False) -> Tuple[str, Any, int]`

Sends a GET request to the specified URL.

- `url`: The URL to send the request to.
- `key`: The authorization key.
- `should_fail`: If `True`, the test will pass if the request fails.

### `put(url: str, body: Optional[str] = None, key: Optional[str] = None, should_fail: bool = False) -> Tuple[str, Any, int]`

Sends a PUT request to the specified URL.

- `url`: The URL to send the request to.
- `body`: The request body.
- `key`: The authorization key.
- `should_fail`: If `True`, the test will pass if the request fails.

### `delete(url: str, key: Optional[str] = None, should_fail: bool = False) -> Tuple[str, Any, int]`

Sends a DELETE request to the specified URL.

- `url`: The URL to send the request to.
- `key`: The authorization key.
- `should_fail`: If `True`, the test will pass if the request fails.

### `run_test(description: str, response: Tuple[str, Any, int], extract: Optional[str] = None) -> Any`

Runs a test and displays the results.

- `description`: The test description.
- `response`: The response from the request function.
- `extract`: The key to extract from the response body.

## Example

```python
if __name__ == "__main__":
    run_test("创建string类型的桶", post("http://localhost:5090/bucket/test-string/string"))
    run_test("创建seq类型的桶", post("http://localhost:5090/bucket/test-seq/seq"))
    run_test("创建time类型的桶", post("http://localhost:5090/bucket/test-time/time"))
    run_test("创建test桶", post("http://localhost:5090/bucket/test/seq"))

    run_test("查看所有的桶", get("http://localhost:5090/bucket"))

    run_test("修改桶名", put("http://localhost:5090/bucket/test/test-new"))

    run_test("再次查看所有的桶", get("http://localhost:5090/bucket"))

    run_test("获取桶的类型", get("http://localhost:5090/bucket/type"))

    run_test("删除桶", delete("http://localhost:5090/bucket/test-new"))

    run_test("最后一次查看所有的桶", get("http://localhost:5090/bucket"))

    run_test("向string类型的桶插入数据_1",
             post("http://localhost:5090/kv",
                  body='''{
                             "Bucket": "test-string",
                             "Key": "test-key",
                             "Value": "test-value-1",
                             "Update": true
                           }'''))

    run_test("读取test-string表的所以数据_1", get("http://localhost:5090/kv/all/test-string"))

    run_test("向string类型的桶插入数据_2",
             post("http://localhost:5090/kv",
                  body='''{
                             "Bucket": "test-string",
                             "Key": "test-key",
                             "Value": "test-value-2",
                             "Update": true
                           }'''))

    run_test("读取test-string表的所以数据_2", get("http://localhost:5090/kv/all/test-string"))

    run_test("向string类型的桶插入冲突数据_3",
             post("http://localhost:5090/kv",
                  should_fail=True,
                  body='''{
                             "Bucket": "test-string",
                             "Key": "test-key",
                             "Value": "test-value-3",
                             "Update": false
                           }'''))

    run_test("读取test-string表的所以数据_3", get("http://localhost:5090/kv/all/test-string"))

    run_test("向seq类型的桶插入数据",
             post("http://localhost:5090/kv",
                  body='''{
                             "Bucket": "test-seq",
                             "Value": "test-value"
                           }'''))

    run_test("读取test-seq表的所以数据", get("http://localhost:5090/kv/all/test-seq"))

    run_test("向time类型的桶插入数据",
             post("http://localhost:5090/kv",
                  body='''{
                             "Bucket": "test-time",
                             "Value": "test-value"
                           }'''))

    total = run_test("读取test-time表的所以数据", get("http://localhost:5090/kv/all/test-time"), extract="total")
    print(f"total={total}\n")
```
