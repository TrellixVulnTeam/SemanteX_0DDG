import os
import requests
import pandas as pd
import openpyxl as pxl
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
    for web_site in search(query, tld="com", lang='en', start=start, stop=stop, pause=pause):
        references[index] = web_site
        index += 1
    return references


def get_text_list(links):
    result = []
    for link in links:
        article = get_article(link)
        clean_text = remove_stopwords(article)
        text = {
            "Link": link,
            "Text": clean_text
        }
        result.append(text)
    return result


def write_to_file(list):
    writer = pd.ExcelWriter('dataset.xlsx', engine='openpyxl')
    if os.path.exists('dataset.xlsx'):
        book = pxl.load_workbook('dataset.xlsx')
        writer.book = book
    text_sheet = pd.DataFrame(list)
    text_sheet.to_excel(writer, sheet_name='Web')
    writer.save()
    writer.close()


def get_data_from_Web(query, number):
    links = search_info(query, 10, number, 15)
    text_list = get_text_list(links)
    write_to_file(text_list)
