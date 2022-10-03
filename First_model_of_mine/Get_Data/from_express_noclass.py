import re
from builtins import type
import pandas as pd

from bs4 import BeautifulSoup

import requests
from prometheus_client.decorator import getfullargspec


def get_link(topic_link):
    topicurl = requests.get(topic_link)
    topic = BeautifulSoup(topicurl.content)
    links = topic.findAll('article', attrs={'class': 'item-news item-news-common '})
    # for link in links:


# print (link)


def get_website(link):
    url = requests.get(link)
    news = BeautifulSoup(url.content)
    return news


def get_data(news) -> dict:
    get_title = news.find('h1').text
    get_description = news.find('p', attrs={'class': 'description'}).text
    get_detail = news.find('article', attrs={'class': 'fck_detail'})
    get_text = get_detail.findAll('p', attrs={'class': 'Normal'})
    data = {}
    data['title'] = get_title
    data['description'] = get_description
    data['content'] = ''
    for item in get_text:
        data['content'] += item.text
    print(data)


def save_data(data, filepath):
    file = open(filepath, 'a')
    file.write(data)
    file.close()


filepath = '/NLP/First_model_of_mine/Get_Data/dataset.txt'
link = 'https://vnexpress.net/nga-dieu-tra-khung-bo-quoc-te-vu-ro-ri-nord-stream-4517046.html'
news = get_website(link)
get_data(news)
# save_data(data, filepath)
# df = pd.DataFrame(data)
# print(df)
