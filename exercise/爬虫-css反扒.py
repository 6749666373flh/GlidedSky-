"""
css反扒
"""

import re

import aiohttp
import asyncio
from bs4 import BeautifulSoup
import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

headers = {
    "Cookie": "footprints=eyJpdiI6IkZta251YTlXRDFtNGMySzByOUxjK0E9PSIsInZhbHVlIjoiVmdLUWJDTnM4MXIrb3U2UytLaTNUaXlJWHJlSEhWM1ZhaXdqTE9DczhHRlFldENtcTRpQXExeVZ5UEdpUVFKaSIsIm1hYyI6IjE2ZTZkNzI4ZmI4MmVlZTc4M2VhNGNjYjljOTUzMjgwYjUyYmQwOGFlNWY0MzAyMzhhZGJiZTU1Zjg1NmU0ZmMifQ%3D%3D; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6ImNQeWlhXC9KQlIxZHE1WW5RbmZFc1JRPT0iLCJ2YWx1ZSI6InVVOVdzNVFtSFJYVjhnV0JhaG1mTkVrcWRlNXhvOVwvQ3ZKY3dTZjNcL0VCKzVrXC9CN2N1aG5qZE5ZYWRUb2hOdVhmcWJUZW5uNEhlVmUyVzBmWG1DKzgwemxScHI3Zm1rcHFDOWZ5NmNhbjU3NVpCeTUrclRlYW9cLzJNTVVRZnY4dUxyUWI1MlVodFNWUDF1WGFDNFlkT2RZanJQTUVuNGJUc1Fpa3N3NXAxR0k9IiwibWFjIjoiNjA1ZDIwZDBiZWI3Yjc2MWU4MWNmM2QxMDY5MjJmMDE1NDI2ODc2NGZiZjgyODQ5OWQ5OGM1MWQ0Y2YxNDAxOCJ9"
}


async def get_page_sum(i, session):
    url = f"http://www.glidedsky.com/level/web/crawler-css-puzzle-1?page={i}"
    total = 0
    async with session.get(url, headers=headers) as resp:
        # print(html)
        html = await resp.text()
        bs = BeautifulSoup(html, "lxml")
        div_list = bs.find_all("div", class_="col-md-1")
        # print(len(div_list))
        for div in div_list:
            div_num_list = div.find_all("div")
            # print(len(div_num_list))
            if len(div_num_list) <= 2:
                for div_num in div_num_list:
                    num_css = div_num['class'][0]
                    res = re.search(rf'\.{num_css}:before.*?content:"(.*?)"', html)
                    if res is not None:
                        num = res.group(1)
                total += int(num)
            else:
                nums = [-1, -1, -1]
                index = 0
                for div_num in div_num_list:
                    num_css = div_num['class'][0]
                    if re.search(rf"\.{num_css}(.*?)margin-right:", html): continue
                    num_text = div_num.text
                    # print(num_css, num_text)
                    res = re.search(rf"\.{num_css}(.*?)left:(.*?)em", html)
                    if res is None:
                        nums[index] = int(num_text)
                    else:
                        nums[index + int(res.group(2))] = int(num_text)
                    index += 1
                num = "".join(str(nu) for nu in nums)
                total += int(num)

    print(f"第{i}页total:{total}")
    return total


async def main():
    # 19.477771043777466
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1000):
            tasks.append(asyncio.ensure_future(get_page_sum(i + 1, session)))

        await asyncio.wait(tasks)
        total = 0
        for task in tasks:
            total += task.result()
        print(total)

if __name__ == '__main__':
    start = time.time()
    # pool = ThreadPoolExecutor(50) # 30.028692960739136
    # pool = ThreadPoolExecutor(100) # 19.08267092704773
    # fs = []
    # for i in range(1000):
    #     fs.append(pool.submit(get_page_sum, i+1))
    #
    # total = 0
    # for f in fs:
    #     total += f.result()
    #
    # print(total)
    # asyncio.run(main())
    print(time.time() - start)
