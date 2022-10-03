import re
import concurrent
import pandas as pd
import requests
from bs4 import BeautifulSoup
from multiprocessing import Process
import hashlib

dict = {'title': [], 'description': [], 'topic': []}
failed_links = []


def crawl(links, tl):
    for link in links:
        news = requests.get(link)
        if news.status_code == 200:
            soup = BeautifulSoup(news.content, "html.parser")
            try:
                title = soup.find("h1", class_="title-detail").text
                descriptiont = soup.find("p", class_="description").text
                description = re.sub(r';', '', descriptiont)
                # body = soup.find("article", class_="fck_detail")
                # pchil = body.findChildren("p", class_="Normal", recursive=False)
                # text = ''
                # for child in pchil:
                #     text += child.text
                dict['title'].append(title)
                dict['description'].append(description)
                # data['content'] = text
                dict['topic'].append(tl)
                dict['URL'] = hashlib.md5(link[22:].encode()).hexdigest()
            except:
                failed_links.append(link)


def cr_pm(tl, i):
    extend = ''
    if i >= 2:
        extend = '-p' + str(i)
    url = 'https://vnexpress.net/' + tl + extend
    response = requests.get(url)
    if response.status_code == 200:
        sour_parent = BeautifulSoup(response.content, "html.parser")
        titles = sour_parent.findAll('h2', class_='title-news')
        if titles:
            links = [link.find('a').attrs["href"] for link in titles]
            crawl(links, tl)
        else:
            titles = sour_parent.findAll('h3', class_='title-news')
            links = [link.find('a').attrs["href"] for link in titles]
            crawl(links, tl)


def mul_pro(tl):
    for i in range(1, 21):
        cr_pm(tl, i)


if __name__ == '__main__':
    topic_lists = ['the-gioi', 'the-thao', 'phap-luat']
    processes = []
    for topic in topic_lists:
        mul_pro(topic)
        p = Process(target=mul_pro, args=[topic])
        p.start()
        processes.append(p)
    for process in processes:
        process.join()

    # mul_pro('thoi-su')
# with Pool(6) as pool:
#     pool.map(cr_pm, range(2, 18), chunksize=3)
df = pd.DataFrame(dict)
df.to_csv('/home/code/NLP/First_model_of_mine/Get_Data/data2.csv')
