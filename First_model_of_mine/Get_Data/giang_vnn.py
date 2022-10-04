import datetime
import re
import concurrent
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from multiprocessing import Process
import hashlib

dict = {'inde': [], 'titl': [], 'desc': [], 'cont': [], 'tmup': [], 'tmcr': [], 'topi': []}
failed_links = []
failed_titles = []


def crawl(links, topi):
    domain = 'https://vietnamnet.vn'
    a = 0
    for link in links:
        try:
            news = requests.get(link)
            soup = BeautifulSoup(news.content, "html.parser")
        except:
            news = requests.get(domain + link)
            soup = BeautifulSoup(news.content, 'html.parser')
        try:
            a += 1
            print('processing', a)
            time_up = str(soup.find('div', class_='breadcrumb-box__time').find('span').text)
            tmup = time_up[30:39] + ' ' + time_up[42:47]
            title = soup.find('h1').text
            description = str(soup.find('div', class_='newFeature__main-textBold').text).strip()
            # description = re.sub(r';', '', descriptiont)
            body = soup.find("div", class_="maincontent").find('div')
            pchil = body.findChildren("p", recursive=False)
            text = ''
            for child in pchil:
                text += ' ' + child.text
            dict['tmcr'].append(str(datetime.datetime.now().strftime('%H:%M %d-%m-%Y')))
            dict['tmup'].append(tmup)
            dict['titl'].append(title)
            dict['desc'].append(description)
            dict['cont'].append(text)
            dict['topi'].append(topi)
            dict['inde'].append(hashlib.md5(link[22:].encode()).hexdigest())
        except:
            failed_links.append(link)


def cr_pm(topi, i):
    extend = '-page' + str(i)
    if topi == 1:
        tl = 'the-gioi'
    elif topi == 2:
        tl = 'the-thao'
    elif topi == 3:
        tl = 'phap-luat'
    print('Crawling ' + tl + extend)
    url = 'https://vietnamnet.vn/' + tl + extend
    response = requests.get(url)
    if response.status_code == 200:
        sour_parent = BeautifulSoup(response.content, "html.parser")
        vtitles = sour_parent.findAll('h3', class_='video__related-title vnn-title')
        if i == 0:
            titles = sour_parent.findAll('h3', class_='vnn-title')
        elif i >= 1:
            titles = sour_parent.findAll('h3', class_='feature-box__content--title vnn-title')
        links = [link.find('a').attrs["href"] for link in titles if link not in vtitles]
        crawl(links, topi)


def mul_pro(topi):
    for i in range(0, 1001):
        cr_pm(topi, i)


if __name__ == '__main__':
    for t in range(1,4):
        mul_pro(t)
# topic_lists = ['the-gioi', 'the-thao', 'phap-luat']
# processes = []
# for topic in topic_lists:
#     mul_pro(topic)
#     p = Process(target=mul_pro, args=[topic])
#     p.start()
#     processes.append(p)
# for process in processes:
#     process.join()
# crawl(['https://vietnamnet.vn/khong-quan-iran-duoc-dau-tu-nang-cao-suc-manh-2063822.html'], 1)

# mul_pro('thoi-su')
# with Pool(6) as pool:
#     pool.map(cr_pm, range(2, 18), chunksize=3)
df = pd.DataFrame(dict)
df.to_csv('/home/code/NLP/LSTM/First_model_of_mine/Get_Data/data2.csv')
