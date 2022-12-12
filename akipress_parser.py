import requests
from bs4 import BeautifulSoup
import re
from time import sleep

headers = {"User-Agent": "CrookedHands/2.0 (EVM x8), CurlyFingers20/1;p"}

def get_url():
    set = {"https://analitika.akipress.org/unews/un_post:24799"}
    for page in range(1, 5, 1):
        print(page)
        url = f"https://analitika.akipress.org/page:{page}"
        response = requests.get(url, headers)

        soup = BeautifulSoup(response.text, "html.parser")

        link = ['https://analitika.akipress.org' + x.find_all('a')[2]['href'] for x in soup.find_all("div", class_="rows-news left col-2")]
        set.update(link)
    for i in set:
        yield i

def get_data():
    index = 0
    for url in get_url():

        response = requests.get(url, headers)

        soup = BeautifulSoup(response.text, "html.parser")

        data = soup.find("div", class_="usernews")

        news_topic = "Аналитика"

        if_exists = soup.find("div", class_="intro")


        try:
            if (len(if_exists) > 0):
                # data2 = soup.find("div", class_="news_list")
                news_data = if_exists.find_all("a")
                news_title = soup.find("div", class_="title").text
            else:
                news_data = data.find("div", class_="text")
                news_title = data.find("h1", class_="title").text
        except TypeError:
            news_data = data.find("div", class_="text")
            news_title = data.find("h1", class_="title").text
        text = ""
        for p in news_data:
            if (p.text == "За событиями в Кыргызстане следите в Телеграм-канале @akipress."):
                continue
            text += p.text
        if (len(text) > 0):
            index += 1
            yield index, url, news_title, text.strip(), news_topic
