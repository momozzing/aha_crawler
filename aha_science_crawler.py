import os
import requests
import ftfy
from datetime import date, timedelta
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
import random
import json
from stem import Signal
from stem.control import Controller
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

'''
23.06.24.21:20  
과학분야 4785 Page
HTML에 최대 몇 페이지인지 나옴
'''
cnt = 0
for i in tqdm(range(1,4785)):
    output = requests.get(
            f"https://www.a-ha.io/questions/categories/73?page={i}&status=published&order=recent",
            # headers=headers, 
            # proxies= proxies,
            ).text
    
    soup = BeautifulSoup(output, 'html.parser')
    #__layout > div > div.base > div.page-container.-pt.page > section > div > main > div > div.md\:tw-w-3\/4.md\:tw-pr-4 > div:nth-child(2) > div:nth-child(1) > div > article > div > header > a
    my_titles = soup.select("head > script") #아이디로 태그 찾음

    data = {}
    for title in my_titles:
        aha_url_list = title.text

    json_data = json.loads(aha_url_list)
    # print(json_data["mainEntity"]['itemListElement'])
    json_data = json_data["mainEntity"]['itemListElement']
    for i in json_data:
        aha_url = i["url"]
        
        output = requests.get(
                aha_url,
                # headers=headers, 
                # proxies= proxies,
                ).text
        output = ftfy.fix_encoding(output)
        open(f"science/page/{cnt}.html", "w").write(output)
        cnt += 1