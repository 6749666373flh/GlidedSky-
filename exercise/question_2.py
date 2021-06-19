import gevent
from gevent import monkey;

monkey.patch_all()
import requests
from bs4 import BeautifulSoup
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48",
    "Cookie": "footprints=eyJpdiI6Ill5bTBQTUZqbVJrQTBLU1VtdEZucFE9PSIsInZhbHVlIjoicTErWnA2WnJIZDV0ZXdIa"
              "VNjbmdRcElIdmlkT0ZEVWlybWpsTG1KNHhJN2pjWERhVlhNb1pmb2U0NXd6MXgxZSIsIm1hYyI6ImI2NjM5NGIzNz"
              "QzNjBjMTVjMDY3Y2ZiYjM1MWI0ZjJhMjkwNTY3OWUwMTk2ZTRhYTViOWI1Y2VjNGFiY2VlOGQifQ==; XSRF-TOKEN"
              "=eyJpdiI6InNLNTdHM2pwemVvMUxoTHM4TXRkQUE9PSIsInZhbHVlIjoidE0yUWpSUjZmc0tvejlzVWVTR0dKUVwvQm"
              "JIS1JtYTVZWW16cTJQK2V0c0tHNG5ScXVhcmhMZXg0ZmJvV01idG0iLCJtYWMiOiJlMmJkZGIwZjIyNDgyZWMxZDlhM"
              "DI1MjY1ZjRmMzIxM2FlMzEzOGY3NjRkNjNiN2JlNzMwZDZlMjI1NWFkZTA2In0=; glidedsky_session=eyJpdiI6"
              "IkdUd0M0MTBZSWxNc0FkZmVSMTZTK3c9PSIsInZhbHVlIjoiREhSN3lWanlOQzJ5amF3SjZxNmNuc3UwY3NsdWdpWkwyTVg3TlJicm9HdnhkRHpNTnR"
              "TK2pNaFwvMVlLNkF2SVciLCJtYWMiOiI0YjhjNWRjZmI3YjQwNjhlNTM1ZjgyMzk4MTc0ZmQyMWFiOTU3MjE3NmZiN2NkMzFlOTFmNmIxODVmYTYxN2NiIn0="}


def get_result(url):
    total = 0
    with requests.get(url, headers=headers) as resq:
        html = resq.text
        html = etree.HTML(html)
        divs = html.xpath("/html/body/div[1]/main/div[1]/div/div/div/div")
        for div in divs:
            total += int(div.text.strip())
    return total


if __name__ == '__main__':
    g_list = []
    for i in range(1001):
        g_list.append(gevent.spawn(get_result, f"http://www.glidedsky.com/level/web/crawler-basic-2?page={i}"))
    gevent.joinall(g_list)

    total = 0
    for g in g_list:
        total += g.value

    print(total)
