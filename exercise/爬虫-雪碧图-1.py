import requests
import re
from lxml import etree
from PIL import Image
import base64
import io
from concurrent.futures import ThreadPoolExecutor, as_completed

headers = {
    "Cookie": "footprints=eyJpdiI6IkluVHphZGx3Y0xaQXNYWHlma2YzbUE9PSIsInZhbHVlIjoiWTFzK2JLZlZCSXl0RHVRbTdjQ0FjUmZJTEpJTHZPMko4S25ibkdjXC8wNFlaSWxTUGx2XC9IdW9FZm5menVsYjYrIiwibWFjIjoiYzM2NDczNDFkOWVkNTNiMzc0MmVhZGQ3NDliOTRlZWE1ZDBjMTlkMDI0MDEwNmFmYTZjN2FmZjVlZTQ2ZjJmZCJ9; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6Ikl5TzgzUG9nVGloTEErMU01cWQzZUE9PSIsInZhbHVlIjoiY0N3UUFpZWNicjlYNlZsRmVYZmVFZ3YxUTVQVStOa0w4TDEyelBHd2lld0p3UGFKODd3S3YzcUtGVithMmxYNmtKSUlqZXJPM1NlMzJwXC9kYVVGcmx5ZGdvNFVRMTREMjN1ZmhZOXV0ZnpoOU5WeG83Z2xJMysxT3lHR1FpS29YZUFCalhXazRZK2kzTlU1ZDFIV3g1M28xUHJPQVl5N1V0TnVYaFB6RFVCOD0iLCJtYWMiOiIzN2ExYzlhNWNiM2I4OWIzN2M1MjY0MGZkYzdlMTBmMWQxOWY4YTE4NjgwY2VjOTdkOWE4YTE2MjE0NGNlZTBmIn0%3D; XSRF-TOKEN=eyJpdiI6IjZMU25pblBjTzR5aHBrMEVnYVNGeHc9PSIsInZhbHVlIjoiQzl0dEwyMEFhakNTcytWcExNTlJ3V2lcL0s4ODNtaThEd21LMVBOeDlrREZkXC94eEZPNUVuQ1RoM2Q2eFRDZnFhIiwibWFjIjoiN2MxOWI5MjljMmYwZDZmMzlkMGQ3OWYyNmRiN2MxNGVjZDQwODEzMDk0MWVkOGRlNDU5Y2UwNWQyNzIxYjU3ZSJ9; glidedsky_session=eyJpdiI6ImhGa3pEOFk1XC82enBZOVdvSUN2NEl3PT0iLCJ2YWx1ZSI6Ikg0eFBLZStnT3hrcThxcHl4REd0UzYwVzdpcnRoNUxkWWZzdEh2Qm5qT05WaW9OcVIyWUl4Q0NqcFR0K2FKb2QiLCJtYWMiOiJlNjZjNjJiZmI3NTVjMzRiOTMyMTA4YzQ1MGMzOWUwNTI1NjA2NzQwNThiZDIzYTU1Y2NkM2I5ZDgwMWI0NjdkIn0%3D",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48",

}


def get_img_sli(html):
    img_base64 = re.search(r'background-image:url\("data:image/png;base64,(?P<img_base64>.*?)"\) }', html).group(
        "img_base64")
    # print(img_base64)
    img_data = base64.b64decode(img_base64)

    img = Image.open(io.BytesIO(img_data))
    width, height = img.size
    # print(width / 10)
    return width / 10


def get_num_dic(div_num_list, html, gap, idx):
    """
    :param idx:
    :param html:
    :param div_num_list: 所有的div
    :param gap: css position 间隔平均值
    :return: css position: 对应数字 =>字典
    """
    num_set = []
    for div_num in div_num_list:
        divs = div_num.xpath('./div')
        for div in divs:
            div_class = div.get("class").split(" ")[0]
            # print(div_class)
            position = re.search(rf'{div_class}.*?background-position-x:(.*?)px', html).group(1)
            num_set.append(abs(int(position)))
    num_set = sorted(list(set(num_set)))
    # print(num_set)
    if len(num_set) < 10:
        print(f"第{idx}页数字为:{len(num_set)}")
        if num_set[0] != 0: num_set.insert(0, 0)
        i = 1
        num_set_len = len(num_set)
        # 对中间缺少的数字插入补齐
        while i < num_set_len:
            if num_set[i] - num_set[i-1] > gap*1.5:
                num_set.insert(i, int(gap + num_set[i-1]))
            else:
                i += 1
            num_set_len = len(num_set)
    # print(num_set)
    return {posi: num for num, posi in enumerate(num_set)}


def get_page_total(i):
    url = f"http://www.glidedsky.com/level/web/crawler-sprite-image-1?page={i}"
    with requests.get(url, headers=headers) as req:
        html = req.text
        # print(html)
        html_tree = etree.HTML(html)
        div_num_list = html_tree.xpath('/html/body/div[1]/main/div[1]/div/div/div/div')

        gap = get_img_sli(html)
        num_dic = get_num_dic(div_num_list, html, gap, i)
        # print(num_dic)
        page_total = 0
        for div_num in div_num_list:
            divs = div_num.xpath('./div')
            digit = 0
            for div in divs:
                div_class = div.get("class").split(" ")[0]
                # print(div_class)
                position = re.search(rf'{div_class}.*?background-position-x:(.*?)px', html).group(1)
                num = num_dic[abs(int(position))]
                digit = digit * 10 + num
            # print(digit)
            page_total += digit
        print(f"第{i}页:{page_total}")
        return page_total


if __name__ == '__main__':
    with ThreadPoolExecutor(10) as pool:
        tasks = []
        for index in range(1, 1001):
            tasks.append(pool.submit(get_page_total, index))

        total = 0
        for task in as_completed(tasks):
            total += task.result()
        print(total)
    # get_page_total(169)
# 2446362 2446362 2446362
# 2446420