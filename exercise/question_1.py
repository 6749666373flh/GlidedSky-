import requests
from bs4 import BeautifulSoup
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48",
    "Referer": "http://www.glidedsky.com/level/crawler-basic-1",
    "Cookie": "footprints"
              "=eyJpdiI6Ill5bTBQTUZqbVJrQTBLU1VtdEZucFE9PSIsInZhbHVlIjoicTErWnA2WnJIZDV0ZXdIaVNjbmdRcElIdmlkT0ZEVWlybWpsTG1KNHhJN2pjWERhVlhNb1pmb2U0NXd6MXgxZSIsIm1hYyI6ImI2NjM5NGIzNzQzNjBjMTVjMDY3Y2ZiYjM1MWI0ZjJhMjkwNTY3OWUwMTk2ZTRhYTViOWI1Y2VjNGFiY2VlOGQifQ==; XSRF-TOKEN=eyJpdiI6Ims4OHdpd0M0REVOREd1cVNpeUd4MFE9PSIsInZhbHVlIjoiN3pQVGJ3ZXNxSkRNcmtFQ0NHSWJCQm5JUkMxTkRtVkZDSkc2V2lReWZWVUc0ZmJlYWl6M3QzSlU0SkV2Sk8yMyIsIm1hYyI6ImEyODFmZDdkYzExMWIxNjIwZmVkMGVjYzEyN2RjNzQ2NGIyMjkxNTI5MWNmNzY5ZjhjNWRkYjY4MGNhYjE0NjUifQ==; glidedsky_session=eyJpdiI6Imo0MHBjUGVyQmNBOFhmaGZyYkt6RUE9PSIsInZhbHVlIjoiTytncDY0dFU3SnZlZld1djFBM0NHR1kyc1RDN3hLaldIa1E2c1wvemhWRUhFZW03SzdXSFdOajdRVWJERlQrU2kiLCJtYWMiOiI2ODM0NzI2Mjg5MDFmZTUxOTgwMjNlODM4NWFhMTQxODE0MGNjOGMyZjVkNmVkNzc1MWViZTdlM2Q3NDU4YzlmIn0= "
}

with requests.get("http://www.glidedsky.com/level/web/crawler-basic-1", headers=headers) as resq:
    html = resq.text

bs = BeautifulSoup(html, "lxml")
rows = bs.find("div", class_="row").find_all("div")

total = 0

for row in rows:
    total += int(row.text.strip())

print(total)
