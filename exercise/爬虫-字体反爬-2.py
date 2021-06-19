from fontTools.ttLib import TTFont
import base64
import io
import requests
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import aiohttp
import asyncio

headers = {
    "Cookie": "footprints=eyJpdiI6IkluVHphZGx3Y0xaQXNYWHlma2YzbUE9PSIsInZhbHVlIjoiWTFzK2JLZlZCSXl0RHVRbTdjQ0FjUmZJTEpJTHZPMko4S25ibkdjXC8wNFlaSWxTUGx2XC9IdW9FZm5menVsYjYrIiwibWFjIjoiYzM2NDczNDFkOWVkNTNiMzc0MmVhZGQ3NDliOTRlZWE1ZDBjMTlkMDI0MDEwNmFmYTZjN2FmZjVlZTQ2ZjJmZCJ9; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6Ikl5TzgzUG9nVGloTEErMU01cWQzZUE9PSIsInZhbHVlIjoiY0N3UUFpZWNicjlYNlZsRmVYZmVFZ3YxUTVQVStOa0w4TDEyelBHd2lld0p3UGFKODd3S3YzcUtGVithMmxYNmtKSUlqZXJPM1NlMzJwXC9kYVVGcmx5ZGdvNFVRMTREMjN1ZmhZOXV0ZnpoOU5WeG83Z2xJMysxT3lHR1FpS29YZUFCalhXazRZK2kzTlU1ZDFIV3g1M28xUHJPQVl5N1V0TnVYaFB6RFVCOD0iLCJtYWMiOiIzN2ExYzlhNWNiM2I4OWIzN2M1MjY0MGZkYzdlMTBmMWQxOWY4YTE4NjgwY2VjOTdkOWE4YTE2MjE0NGNlZTBmIn0%3D; XSRF-TOKEN=eyJpdiI6IlBsS3dCWWxYWmFtbFlPajJ6MmN2U2c9PSIsInZhbHVlIjoiM1FLUWsyMkNpTmYwd2U5Z3RCZGpVT2wwYmZ2elpscVwvdWtqU25nK3BNQ3RoXC9QN0VXaWNoeFozTEhPUWJFZGhnIiwibWFjIjoiNDJlMzNhY2UzOTQyOGU4YzY4ZGIyMDA3MWZmNDFkZDc5NzViNzgxNTdjNDI4MDlmNWM4YWM5ZWIxMTkyNTAwNiJ9; glidedsky_session=eyJpdiI6IkprZ0dNcnh4amdodWVwV3RrWFlCQ1E9PSIsInZhbHVlIjoicUpvS051OVpIZzVGdDhlRDdkQ1NSeDA5eW1PdXlGZGZFSGxQMHVnXC8wXC9EWUZcLzN4a2VEOGRKVWJtWUsyMUU4YSIsIm1hYyI6IjhkYjFkYzJlMjQxOWVkZjJiZjRhY2NmYTNhZDU2ZTdiNThkNjRmM2ZiNTA1Mzk1MDlmZjYzZjg0OWQzNDU5ZDEifQ%3D%3D"
}

kangxi = {'一': '⼀', '乙': '⼄', '二': '⼆', '人': '⼈', '儿': '⼉', '入': '⼊', '八': '⼋', '几': '⼏', '刀': '⼑', '力': '⼒', '匕': '⼔',
          '十': '⼗', '卜': '⼘', '厂': '⼚', '又': '⼜', '口': '⼝', '土': '⼟', '士': '⼠', '大': '⼤', '女': '⼥', '子': '⼦', '寸': '⼨',
          '小': '⼩', '尸': '⼫', '山': '⼭', '工': '⼯', '己': '⼰', '干': '⼲', '广': '⼴', '弓': '⼸', '心': '⼼', '戈': '⼽', '手': '⼿',
          '支': '⽀', '文': '⽂', '斗': '⽃', '斤': '⽄', '方': '⽅', '无': '⽆', '日': '⽇', '曰': '⽈', '月': '⽉', '木': '⽊', '欠': '⽋',
          '止': '⽌', '歹': '⽍', '毋': '⽏', '比': '⽐', '毛': '⽑', '氏': '⽒', '气': '⽓', '水': '⽔', '火': '⽕', '爪': '⽖', '父': '⽗',
          '片': '⽚', '牙': '⽛', '牛': '⽜', '犬': '⽝', '玄': '⽞', '玉': '⽟', '瓜': '⽠', '瓦': '⽡', '甘': '⽢', '生': '⽣', '用': '⽤',
          '田': '⽥', '白': '⽩', '皮': '⽪', '皿': '⽫', '目': '⽬', '矛': '⽭', '矢': '⽮', '石': '⽯', '示': '⽰', '禾': '⽲', '穴': '⽳',
          '立': '⽴', '竹': '⽵', '米': '⽶', '缶': '⽸', '网': '⽹', '羊': '⽺', '羽': '⽻', '老': '⽼', '而': '⽽', '耳': '⽿', '肉': '⾁',
          '臣': '⾂', '自': '⾃', '至': '⾄', '舌': '⾆', '舟': '⾈', '艮': '⾉', '色': '⾊', '虫': '⾍', '血': '⾎', '行': '⾏', '衣': '⾐',
          '角': '⻆', '言': '⾔', '谷': '⾕', '豆': '⾖', '赤': '⾚', '走': '⾛', '足': '⾜', '身': '⾝', '车': '⻋', '辛': '⾟', '辰': '⾠',
          '邑': '⾢', '酉': '⾣', '采': '⾤', '里': '⾥', '金': '⾦', '长': '⻓', '门': '⻔', '阜': '⾩', '隶': '⾪', '雨': '⾬', '青': '⻘',
          '非': '⾮', '面': '⾯', '革': '⾰', '韭': '⾲', '音': '⾳', '页': '⻚', '风': '⻛', '飞': '⻜', '食': '⻝', '首': '⾸', '香': '⾹',
          '马': '⻢', '骨': '⻣', '高': '⾼', '鬼': '⻤', '鱼': '⻥', '鸟': '⻦', '卤': '⻧', '鹿': '⿅', '麻': '⿇', '黍': '⿉', '黑': '⿊',
          '鼎': '⿍', '鼓': '⿎', '鼠': '⿏', '鼻': '⿐', '齿': '⻮', '龙': '⻰', '夕': '⼣', '兀': '⺎', '尣': '⺏', '尢': '⺐', '𡯂': '⺑',
          '巳': '⺒', '幺': '⺓', '旡': '⺛', '母': '⺟', '民': '⺠', '冈': '⺱', '芈': '⺸', '虎': '⻁', '西': '⻄', '见': '⻅', '𧢲': '⻇',
          '贝': '⻉', '镸': '⻒', '韦': '⻙', '𩠐': '⻡', '麦': '⻨', '黄': '⻩', '齐': '⻬', '竜': '⻯', '龟': '⻳', '臼': '⾅', '户': '⼾',
          '巾': '⼱'}

def get_page_total(i):
    # print(len(kangxi))
    with requests.get(f"http://www.glidedsky.com/level/web/crawler-font-puzzle-2?page={i}",
                      headers=headers) as resp:
        resp.encoding = "utf-8"
        html = resp.text
        bs = BeautifulSoup(html, "html.parser")
        divs = bs.find("div", class_="row").find_all("div")
        nums = [div.text.strip() for div in divs]
        # print(nums)

        font_base64 = re.search(r''';base64,(.*?)\)''', html).group(1)
        b_data = base64.b64decode(font_base64)
        # with open("tt.ttf", "wb") as f:
        #     f.write(b_data)
        tt_font = TTFont(io.BytesIO(b_data))
        # tt_font.saveXML("tt.xml")
        orders = tt_font.getGlyphOrder()[1:11]
        # print(orders)
        font_dic = {}
        idx = 0
        for order in orders:
            if idx == 10: idx = 0
            key = fr"\u{order[3:]}".encode("utf-8").decode("unicode_escape")
            font_dic[key] = str(idx)
            idx += 1

        # print(font_dic)
        page_total = 0
        for num in nums:
            digit = ''
            # print(num)
            for uni_n in iter(num):
                n = font_dic.get(uni_n)
                if n is None:
                    n = font_dic.get(kangxi.get(uni_n))
                    # if n is not None: print("已查到")
                if n is None:
                    print(f"第-{i}-页出现字体错误")
                    print(uni_n)
                    print(font_dic)
                    print("-------------------")
                    return 0
                digit += n
            # print(digit)
            page_total += int(digit)

        print(f"第{i}页:{page_total}")
        return page_total


def main():
    # tasks = []
    # async with aiohttp.ClientSession() as session:
    #     for i in range(1, 1001):
    # tasks.append(asyncio.create_task(get_page_total(i, session)))

    # await asyncio.wait(tasks)

    pool = ThreadPoolExecutor(5)
    tasks = []
    for i in range(1, 1001):
        tasks.append(pool.submit(get_page_total, i))

    total = 0
    for task in as_completed(tasks):
        total += task.result()
    print(total)
    # get_page_total(1)


if __name__ == '__main__':
    main()
