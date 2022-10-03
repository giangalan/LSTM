import re
from bs4 import BeautifulSoup
import requests
from prometheus_client.decorator import getfullargspec


class DataFromNews:
    def __init__(self, filepath, link):
        self.filepath = filepath
        self.link = link

    def get_website(self):
        url = requests.get(self.link)
        news = BeautifulSoup(url.content)
        return news

    def get_data(self):
        news = self.get_website(self.link)
        get_title = news.find('h1').text
        get_description = news.find('p', attrs={'class': 'description'}).text
        get_detail = news.find('article', attrs={'class': 'fck_detail'})
        get_text = get_detail.findAll('p', attrs={'class': 'Normal'})
        data = {}
        data['titlte'] = get_title
        data['description'] = get_description
        text = []
        for item in get_text:
            text.append(item.text)
        data['content'] = text
        return data

    def save_data(self):
        data = self.get_data(self.link)
        file = open(self.filepath, 'a')
        file.write(data)
        file.close()


if __name__ == '__main__':
    links = 'https://vnexpress.net/nga-dieu-tra-khung-bo-quoc-te-vu-ro-ri-nord-stream-4517046.html'
    DataFromNews('/NLP/First_model_of_mine/Get_Data/dataset.txt', links)
    DataFromNews.save_data()
