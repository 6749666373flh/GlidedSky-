"""
字体反扒_1
"""
from fontTools.ttLib import TTFont
import base64
import io
import requests
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

dic = {'four': 4, 'five': 5, 'nine': 9, 'eight': 8, 'six': 6, 'zero': 0, 'two': 2, 'three': 3, 'one': 1, 'seven': 7}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48",
    'Cookie': '''footprints=eyJpdiI6IkZta251YTlXRDFtNGMySzByOUxjK0E9PSIsInZhbHVlIjoiVmdLUWJDTnM4MXIrb3U2UytLaTNUaXlJWHJlSEhWM1ZhaXdqTE9DczhHRlFldENtcTRpQXExeVZ5UEdpUVFKaSIsIm1hYyI6IjE2ZTZkNzI4ZmI4MmVlZTc4M2VhNGNjYjljOTUzMjgwYjUyYmQwOGFlNWY0MzAyMzhhZGJiZTU1Zjg1NmU0ZmMifQ==; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6ImNQeWlhXC9KQlIxZHE1WW5RbmZFc1JRPT0iLCJ2YWx1ZSI6InVVOVdzNVFtSFJYVjhnV0JhaG1mTkVrcWRlNXhvOVwvQ3ZKY3dTZjNcL0VCKzVrXC9CN2N1aG5qZE5ZYWRUb2hOdVhmcWJUZW5uNEhlVmUyVzBmWG1DKzgwemxScHI3Zm1rcHFDOWZ5NmNhbjU3NVpCeTUrclRlYW9cLzJNTVVRZnY4dUxyUWI1MlVodFNWUDF1WGFDNFlkT2RZanJQTUVuNGJUc1Fpa3N3NXAxR0k9IiwibWFjIjoiNjA1ZDIwZDBiZWI3Yjc2MWU4MWNmM2QxMDY5MjJmMDE1NDI2ODc2NGZiZjgyODQ5OWQ5OGM1MWQ0Y2YxNDAxOCJ9; XSRF-TOKEN=eyJpdiI6InZXWXc5ZXdBS3d6a2g5WStYV0VIRkE9PSIsInZhbHVlIjoiRUc5ZFJnemJnUDg4eGVSREpUYnFWUG10XC9mYVkzTGRvQzl3Um4xcllVT29lRHN3bElsMzFvd1JGSkF3WlFJVzQiLCJtYWMiOiIxMjJiZDI0NmMyNzI5ZWUxMDRjOTc3MTQ4MmE5MWZhNjYxNGI4NjRhNmFmZmZjZGY1NTZmYzFjMTdlMDg3NGI5In0=; glidedsky_session=eyJpdiI6IlJPNTZldkVST2hDSDltOHFJT3A2Qmc9PSIsInZhbHVlIjoiWHRnQk95K2RMWStST0hMM2Z3WmwrUkFMYlFyck0wZkdPSEd3dlFMbzB3djRWS1p1a0FlZVBJWVVzYnllakt1cCIsIm1hYyI6IjljYWI3YmMxMTA1ZWRhOThiOTgwNzJhYTI5ZWRlZDFmOWRjNmFmMDhhMDgwNzg0MjFiNzMyMWY4NGMwYjc1NTMifQ=='''
}


def get_page_sum(i):
    with requests.get(f"http://www.glidedsky.com/level/web/crawler-font-puzzle-1?page={i}", headers=headers) as resp:
        bs = BeautifulSoup(resp.text, "html.parser")
        divs = bs.find("div", class_="row").find_all("div")
        nums = [div.text.strip() for div in divs]
        # print(nums)

        font_base64 = re.search(r''';base64,(.*?)\)''', resp.text).group(1)
        b_data = base64.b64decode(font_base64)

        tt_font = TTFont(io.BytesIO(b_data))
        order = tt_font.getGlyphOrder()[1:]

        font_dic = {}
        for num, pic in enumerate(order):
            key = str(dic.get(pic))
            font_dic[key] = str(num)
        # print(font_dic)

        total = 0
        for num in nums:
            real_num = ""
            for ch in iter(num):
                nu = font_dic.get(ch)
                real_num += nu
            total += int(real_num)

        print(f"第{i}页总数为:{total}")
        return total


if __name__ == '__main__':
    pool = ThreadPoolExecutor(10)
    fs = []
    for i in range(1000):
        fs.append(pool.submit(get_page_sum, i+1))

    total = 0
    for future in as_completed(fs):
        total += future.result()

    print(total)
