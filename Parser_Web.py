import os
import requests
import analyzer
from bs4 import BeautifulSoup as soup
from nltk.corpus import stopwords
from googlesearch import search


def check_directory(name):
    list_files = os.listdir()
    return list_files.count(name) == 0


def create_file(text):
    id = 0
    name = "text_" + str(id) + '.txt'
    exist = check_directory(name)
    while not exist:
        id += 1
        name = "text_" + str(id) + '.txt'
        exist = check_directory(name)
    file = open(name, 'w+')
    for words in text:
        file.write(words)
    file.close()


def remove_stopwords(text):
    stops = set(stopwords.words('english'))
    tokens = text.split(' ')
    for word in tokens:
        for stop in stops:
            if word == stop:
                tokens.remove(word)
    result_text = ' '
    for word in tokens:
        result_text += word + ' '
    return result_text


def get_article(URL):
    page = requests.get(URL, headers={"User-Agent": "Chrome"})
    html = page.text
    page.close()
    page_soup = soup(html, 'html.parser')
    components = page_soup.find_all('p')
    # components = page_soup.find_all('div', {"data-component": 'text-block'})
    content = ''
    for item in components:
        content += item.text + '\n'
    return content


def get_title(URL):
    page = requests.get(URL, headers={"User-Agent": "Chrome"})
    html = page.text
    page.close()
    page_soup = soup(html, 'html.parser')
    return page_soup.h1.text


def search_info(query, start, stop, pause):
    index = 0
    references = [None for i in range(stop)]
    for web_site in search(query, tld="com", num=start, stop=stop, pause=pause):
        references[index] = web_site
        index += 1
    return references


if __name__ == '__main__':
    links = search_info("Samsung Galaxy Note 10", 10, 4, 30)
    for link in links:
        print(link)
        # article = get_article(link)
        # clean_text = remove_stopwords(article)
        # analyzer.TEXT = clean_text
        # create_file(clean_text)