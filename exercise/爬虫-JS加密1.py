import math

import execjs
import hashlib
import aiohttp
import asyncio
from aiohttp import request
import re
import json

from lxml import etree
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

headers = {
    "Cookie": "footprints=eyJpdiI6IkluVHphZGx3Y0xaQXNYWHlma2YzbUE9PSIsInZhbHVlIjoiWTFzK2JLZlZCSXl0RHVRbTdjQ0FjUmZJTEpJTHZPMko4S25ibkdjXC8wNFlaSWxTUGx2XC9IdW9FZm5menVsYjYrIiwibWFjIjoiYzM2NDczNDFkOWVkNTNiMzc0MmVhZGQ3NDliOTRlZWE1ZDBjMTlkMDI0MDEwNmFmYTZjN2FmZjVlZTQ2ZjJmZCJ9; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6Ikl5TzgzUG9nVGloTEErMU01cWQzZUE9PSIsInZhbHVlIjoiY0N3UUFpZWNicjlYNlZsRmVYZmVFZ3YxUTVQVStOa0w4TDEyelBHd2lld0p3UGFKODd3S3YzcUtGVithMmxYNmtKSUlqZXJPM1NlMzJwXC9kYVVGcmx5ZGdvNFVRMTREMjN1ZmhZOXV0ZnpoOU5WeG83Z2xJMysxT3lHR1FpS29YZUFCalhXazRZK2kzTlU1ZDFIV3g1M28xUHJPQVl5N1V0TnVYaFB6RFVCOD0iLCJtYWMiOiIzN2ExYzlhNWNiM2I4OWIzN2M1MjY0MGZkYzdlMTBmMWQxOWY4YTE4NjgwY2VjOTdkOWE4YTE2MjE0NGNlZTBmIn0%3D; XSRF-TOKEN=eyJpdiI6IjZ2UkdLT0pXU0tZNGk1ZzFWQXQ1MUE9PSIsInZhbHVlIjoiN3BET1RtQzJRRHhNWHBaNVdJUm41NExpMWNzZjJxQ0JXMEZcLzdNTXBmbndLcGd1NGhwODM2Sm5mUHNPU2lrWVciLCJtYWMiOiI2ZTZiNzMwNWRiOTNjYzBkY2EzZDU3OWZmYzY0N2YxMjkzNjdhZDNmNGNiMjYzNzdkNTg5ODdkZjgxNDExZWU4In0%3D; glidedsky_session=eyJpdiI6InJyXC9nUDd6ZkNKRVwvbVF2NE5hVG5wZz09IiwidmFsdWUiOiJ5T3ZsbFFmR2NydkdzWlJybm9KZTV0a0xkQUJQRmpQQU5BSk9nOVFHaGQ5eGVCMlZiQTFjbnZ0dHk0cGpsdGYzIiwibWFjIjoiM2QyYWQ0NmRmNDhmNjdlOTFlODY5MDBlNTU2MzdhY2Q4Nzg5YTNjYzBhNmQwZWNlYjNmMzFlZmM4ZGZjYjBkYyJ9"
}


def get_sign(t):
    """
    返回加密参数sign
    :param t:
    :return: sign
    """
    sha1 = hashlib.sha1(f'Xr0Z-javascript-obfuscation-1{t}'.encode("utf-8"))
    return sha1.hexdigest()


def get_t(html):
    """
    返回参数t
    :param html: 页面
    :return: 参数t
    """
    tree_html = etree.HTML(html)
    div = tree_html.xpath("/html/body/div[1]/main/div[1]")[0]
    t = div.get("t")
    t = math.floor((int(t) - 99) / 99)
    return t


def get_page_total(i):
    url = f"http://www.glidedsky.com/level/web/crawler-javascript-obfuscation-1?page={i}"

    with requests.get(url, headers=headers) as req:
        t = get_t(req.text)
        params = {
            "page": f"{i}",
            "t": f"{t}",
            "sign": get_sign(t)
        }
        with requests.get(f"http://www.glidedsky.com/api/level/web/crawler-javascript-obfuscation-1/items"
                , params=params) as req1:
            nums = req1.json()["items"]
            total = sum(list(nums))
            print(f"第{i}页总数为:{total}")
    return total


def main():
    total = 0
    pool = ThreadPoolExecutor(50)
    fs = []
    for i in range(1, 1001):
        fs.append(pool.submit(get_page_total, i))

    for f in fs:
        total += f.result()

    print(total)


if __name__ == '__main__':
    main()
