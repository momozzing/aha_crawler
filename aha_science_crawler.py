# -*- coding: utf-8 -*-

import os
import requests
import ftfy
import datetime
from bs4 import BeautifulSoup
from tqdm import tqdm
import json
import xml.etree.ElementTree as ET
from stem import Signal
from stem.control import Controller
from multiprocessing import Pool
import time
import random

# import wandb


## wandb log
# wandb.init(project="note_crawler", name=f"note_crawler")
# Tor 프록시 서버 설정

# def bypass_ip():
#     # Tor 제어를 위한 Controller 객체 생성
#     with Controller.from_port(port=9051) as controller:
#         controller.authenticate(password='momo')

#         # 새로운 IP 주소로 변경
#         controller.signal(Signal.NEWNYM)

beforeCrawling = datetime.datetime.now()
beforeCrawlingTime = beforeCrawling.strftime("%Y-%m-%d %H:%M:%S")
print("크롤링 시작 시간", beforeCrawlingTime)
# rand_value = random.randint(1, 5)
# proxies = {
#     'http': 'socks5://127.0.0.1:9050',
#     'https': 'socks5://127.0.0.1:9050'
# }
# headers={'User-Agent': 'Mozilla/5.0'}

# file_path = "note_test/"

def get_HTML(aha_url):
    # bypass_ip()
    output = requests.get(
            aha_url,
            # headers=headers, 
            # proxies= proxies,
            ).text
    output = ftfy.fix_encoding(output)
    open(f"science/pages/{aha_url.replace('https://', '').replace('/', '-')}.html", "w").write(output)


page_num = 4786
for i in tqdm(range(1,page_num)):
    output = requests.get(
            f"https://www.a-ha.io/questions/categories/73?page={i}&status=published&order=recent",
            # headers=headers, 
            # proxies= proxies,
            ).text
    
    soup = BeautifulSoup(output, 'html.parser')
    #__layout > div > div.base > div.page-container.-pt.page > section > div > main > div > div.md\:tw-w-3\/4.md\:tw-pr-4 > div:nth-child(2) > div:nth-child(1) > div > article > div > header > a
    my_titles = soup.select("head > script") #아이디로 태그 찾음

    for title in my_titles:
        aha_url_list = title.text

    json_data = json.loads(aha_url_list)
    # print(json_data["mainEntity"]['itemListElement'])
    json_data = json_data["mainEntity"]['itemListElement']

    for i in json_data:
        aha_url = []
        aha_url.append(i["url"])

        with Pool(processes=20) as pool:
            pool.map(get_HTML, aha_url)

afterCrawling = datetime.datetime.now()
afterCrawlingTime = afterCrawling.strftime("%Y-%m-%d %H:%M:%S")                   
print("크롤링 종료 시간", afterCrawling)