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
import pandas as pd



# science # page_num=4786
# 48%|████████████████████████████▌                              | 2313/4785 [1:14:40<1:19:48,  1.94s/it]
# 35%|██████████████████████▏                                         | 855/2473 [28:28<53:52,  2.00s/it]

# tip  # page_num=16236
# 6%|███▍                                                        | 926/16235 [40:11<11:04:23,  2.60s/it]
#  9%|█████▏                                                   | 1397/15310 [1:07:46<11:14:59,  2.91s/it]
# 18%|██████████▋                                               | 2639/14384 [1:27:37<6:29:57,  1.99s/it]
# 24%|█████████████▊                                            | 2806/11745 [1:23:33<4:26:11,  1.79s/it]
#  35%|████████████████████▍                                      | 3101/8939 [2:04:10<3:53:45,  2.40s/it]

# gomin # page_num= 674 
#  1%|▍                                                                  | 5/674 [00:05<12:58,  1.16s/it]
# pet # page_num = 1712  
#  8%|████▎                                                | 138/1711 [06:55<1:18:50,  3.01s/it]
# clean # page_num = 234
# laundry # page_num = 263

data = pd.read_csv("aha_info-2.csv", delimiter=",") # 650이 넘지않는 재무설계, 무역 뺀것
data = data[20:]
print(data)
for i in range(0, 25-2-20):
    domain_name = data.iloc[i][0]
    domain_num = data.iloc[i][1]
    # page_num = data.iloc[i][3]
    page_num = 650

    

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
# 73: 과학 52: 생활꿀팁 106: 고민상담 68: 반려동물 98: 청소 102: 세탁

# domain_num = 73
# domain_name = "과학"
# page_num = 263

def get_HTML(aha_url):
    # bypass_ip()
    output = requests.get(
            aha_url,
            # headers=headers, 
            # proxies= proxies,
            ).text
    output = ftfy.fix_encoding(output)
    os.makedirs(f"{domain_name}/pages", exist_ok=True)
    open(f"{domain_name}/pages/{aha_url.replace('https://', '').replace('/', '-')}.html", "w").write(output)

def get_link(output):
        soup = BeautifulSoup(output, 'html.parser')
        #__layout > div > div.base > div.page-container.-pt.page > section > div > main > div > div.md\:tw-w-3\/4.md\:tw-pr-4 > div:nth-child(2) > div:nth-child(1) > div > article > div > header > a
        my_titles = soup.select("head > script") #아이디로 태그 찾음

        # my_titles = soup.select('script', attrs={'type': 'application/ld+json'})
        # print(my_titles)
        
        for title in my_titles:
            global aha_url_list
            aha_url_list = title.text
            # print(aha_url_list)

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
        
        
    for i in range(0, 25-2-20):
        domain_name = data.iloc[i][0]
        domain_num = data.iloc[i][1]
        page_num = 650
        
        beforeCrawling = datetime.datetime.now()
        beforeCrawlingTime = beforeCrawling.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{domain_name} 크롤링 시작 시간", beforeCrawlingTime)
        
        for i in tqdm(range(1,page_num)):
            output = requests.get(
                    f"https://www.a-ha.io/questions/categories/{domain_num}?page={i}&status=published&order=recent", ## 일반적인거 
                    # f"https://www.a-ha.io/questions/categories/{domain_num}?page={i}&status=published&order=recent",
                    # f"https://www.a-ha.io/questions/categories/{domain_num}?page={i}&status=waiting&status=ready&status=outdated&order=recent", ## 청소
                    # headers=headers, 
                    # proxies= proxies,
                    ).text
            
            # print(get_link(output))
            with Pool(processes=10) as pool:
                pool.map(get_HTML, get_link(output))
        
        
        afterCrawling = datetime.datetime.now()
        afterCrawlingTime = afterCrawling.strftime("%Y-%m-%d %H:%M:%S")                   
        print(f"{domain_name}크롤링 종료 시간", afterCrawling)
        
    afterCrawling = datetime.datetime.now()
    afterCrawlingTime = afterCrawling.strftime("%Y-%m-%d %H:%M:%S")                   
    print(f"크롤링 종료 시간", afterCrawling)