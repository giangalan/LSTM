# import re
# import concurrent
import pandas as pd
import requests
from bs4 import BeautifulSoup
from multiprocessing import Process
# import hashlib

dict = {'topic': [], 'title':[], 'content':[] }
failed_links = []


def crawl(links, tl):
    for link in links:
        news = requests.get(link)
        print("Crawling ",link)
        if news.status_code == 200:
            soup = BeautifulSoup(news.content, "html.parser")
            try:
                title = soup.find("h1", class_="title-detail").text
                # descriptiont = soup.find("p", class_="description").text
                # description = re.sub(r';', '', descriptiont)
                body = soup.find("article", class_="fck_detail")
                if body:
                    pchil = body.findChildren("p", class_="Normal", recursive=False)
                    text = ''
                    for child in pchil:
                        text += child.text
                else:
                    body = soup.find("div", class_="desc_cation")
                    pchil = body.findChildren("p", class_="Normal", recursive=False)
                    text = ''
                    for child in pchil:
                        text += child.text
                dict['title'].append(title)
                # dict['description'].append(description)
                dict['content'].append(text)
                dict['topic'].append(tl)
                # dict['URL'] = hashlib.md5(link[22:].encode()).hexdigest()
            except:
                failed_links.append(link)


def cr_pm(topic_list, num_page):
    extend = ''
    if num_page >= 2:
        extend = '-p' + str(num_page)
    url = 'https://vnexpress.net/' + topic_list + extend
    response = requests.get(url)
    if response.status_code == 200:
        sour_parent = BeautifulSoup(response.content, "html.parser")
        titles = sour_parent.findAll('h1', class_='title-news')
        if titles:
            links = [link.find('a').attrs["href"] for link in titles]
            crawl(links, topic_list)
        titles = sour_parent.findAll('h3', class_='title-news')
        links = [link.find('a').attrs["href"] for link in titles]
        crawl(links, topic_list)


def mul_pro(topic_list):
    for num_page in range(1, 20):
        cr_pm(topic_list, num_page)


if __name__ == '__main__':
    topic_lists = ['the-gioi', 'the-thao', 'khoa-hoc','giai-tri','kinh-doanh','phap-luat','giao-duc','suc-khoe']
    processes = []
    for topic in topic_lists:
        mul_pro(topic)
        p = Process(target=mul_pro, args=[topic])
        p.start()
        processes.append(p)
    for process in processes:
        process.join()


df = pd.DataFrame(dict)
df.to_csv('./data.csv')