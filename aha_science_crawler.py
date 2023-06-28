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
# science # page_num=4786
# 48%|████████████████████████████▌                              | 2313/4785 [1:14:40<1:19:48,  1.94s/it]
# 35%|██████████████████████▏                                         | 855/2473 [28:28<53:52,  2.00s/it]

# tip  # page_num=16236
 #6%|███▍                                                        | 926/16235 [40:11<11:04:23,  2.60s/it]
# 6%|███▍                                                        | 926/16235 [40:11<11:04:23,  2.60s/it]
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


# rand_value = random.randint(1, 5)
# proxies = {
#     'http': 'socks5://127.0.0.1:9050',
#     'https': 'socks5://127.0.0.1:9050'
# }
# headers={'User-Agent': 'Mozilla/5.0'}

# file_path = "note_test/"
## 73: 과학 52 생활꿀팁
def get_HTML(aha_url):
    # bypass_ip()
    output = requests.get(
            aha_url,
            # headers=headers, 
            # proxies= proxies,
            ).text
    output = ftfy.fix_encoding(output)
    open(f"tip/pages/{aha_url.replace('https://', '').replace('/', '-')}.html", "w").write(output)

def get_link(output):
        soup = BeautifulSoup(output, 'html.parser')
        #__layout > div > div.base > div.page-container.-pt.page > section > div > main > div > div.md\:tw-w-3\/4.md\:tw-pr-4 > div:nth-child(2) > div:nth-child(1) > div > article > div > header > a
        my_titles = soup.select("head > script") #아이디로 태그 찾음

        for title in my_titles:
            global aha_url_list
            aha_url_list = title.text

        json_data = json.loads(aha_url_list)
        # print(json_data["mainEntity"]['itemListElement'])
        json_data = json_data["mainEntity"]['itemListElement']
        aha_url = []
        for i in json_data:
            # aha_url = i["url"]
            aha_url.append(i["url"])
            # get_HTML(aha_url)
        
        return aha_url
            
            # with Pool(processes=100) as pool:
            #     pool.map(get_HTML, aha_url)
            # with Pool(processes=20) as pool:
            #     pool.map(get_HTML, aha_url)
        
if __name__=="__main__":
    beforeCrawling = datetime.datetime.now()
    beforeCrawlingTime = beforeCrawling.strftime("%Y-%m-%d %H:%M:%S")
    print("크롤링 시작 시간", beforeCrawlingTime)
    
    page_num = 16236
    for i in tqdm(range(926+926+2639,page_num)):
        output = requests.get(
                f"https://www.a-ha.io/questions/categories/52?page={i}&status=published&order=recent",
                # headers=headers, 
                # proxies= proxies,
                ).text
        
        # print(get_link(output))
        with Pool(processes=10) as pool:
            pool.map(get_HTML, get_link(output))
    
    
    afterCrawling = datetime.datetime.now()
    afterCrawlingTime = afterCrawling.strftime("%Y-%m-%d %H:%M:%S")                   
    print("크롤링 종료 시간", afterCrawling)