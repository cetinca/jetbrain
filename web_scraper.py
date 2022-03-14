import sys
import time
import requests
from bs4 import BeautifulSoup
import os

page_number = int(input())
article_type = input()

for i in range(1, page_number + 1):
    dir_name = f"./Page_{str(i)}"
    os.mkdir(dir_name)

    domain = "https://www.nature.com"
    url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page="

    try:
        r = requests.get(url + str(i))
    except TimeoutError:
        print("Invalid page!")
        sys.exit()

    if r.status_code != 200:
        print(f"The URL returned {r.status_code}")
        sys.exit()
    else:
        content = r.content
        with open("source.html", "wb") as file:
            file.write(content)

    with open("source.html", "rb") as file:
        content = file.read()
    #
    soup = BeautifulSoup(content, 'html.parser')

    mapdict = {" ": "_", ":": None, "?": None}
    mapping_table = "".maketrans(mapdict)
    article_dict = {}


    def get_article_content(_link):
        _r = requests.get(_link)
        _content = _r.content
        _soup = BeautifulSoup(_content, 'html.parser')
        _body = _soup.find('div', attrs={'class': "c-article-body"})
        return _body.text.strip()


    articles = soup.find_all("li", {"class": "app-article-list-row__item"})
    for article in articles:
        if article.find("span", {"class": "c-meta__type"}).text == article_type:
            art = article.find("a").text
            link = domain + article.find("a")["href"]
            art = art.translate(mapping_table)
            art_body = get_article_content(link)
            article_dict.update({art: art_body})

    for k, v in article_dict.items():
        with open(f"{dir_name}/{k}.txt", "w", encoding="utf-8", newline="") as file:
            file.write(v)

    time.sleep(1)

print("Saved all articles.")
