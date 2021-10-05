# --*-- coding: utf-8 --*--
import requests
import parsel
from urllib.parse import urljoin
import pandas as pd
import datetime
import os

base_path = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_path,'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

cookies = {
    '_csrf': '2ae487e076b69b7524c21e10c1aeea43c3f28cdef8c5a4e2ce62a16fcbd4f582',
    '_lxsdk_s': '17c4e1a1077-e5-7fd-209%7C%7C46',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'https://maoyan.com/news',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}
base_url = 'http://www.maoyan.com'
response = requests.get('https://maoyan.com/board',
                        headers=headers, cookies=cookies)
# print(response.text)
df = pd.DataFrame()
selector = parsel.Selector(response.text)
for info in selector.css("dl.board-wrapper dd"):
    item = {}
    item['title'] = info.css("p.name a::attr(title)").get()
    item['href'] = urljoin(base_url, info.css("p.name a::attr(href)").get())
    item['star'] = info.css("p.star::text").get().strip()
    item['releasetime'] = info.css(
        "p.releasetime::text").re(r"(\d{4}-\d{2}-\d{2})")[0]
    item['score'] = "".join(info.css("p.score i::text").getall())
    print(item)
    df = df.append(item, ignore_index=True)


date = datetime.date.today()
print(df)
df.to_csv(f"{data_dir}/{date}猫眼.csv", index=0)
