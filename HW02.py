# Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ и извлечь 
# информацию о всех книгах на сайте во всех категориях: название, цену, количество товара 
# в наличии (In stock (19 available)) в формате integer, описание.

# Затем сохранить эту информацию в JSON-файле.

import requests
from bs4 import BeautifulSoup
import urllib.parse as prs
import re
import json
import time

url_1 = 'https://books.toscrape.com/'
# all_book = {}
all_book = []

url = 'https://books.toscrape.com/'

while True:
    response = requests.get(url)
    page  = BeautifulSoup(response.content, 'html.parser')
    result = page.find_all('li', ('class', 'col-xs-6 col-sm-4 col-md-3 col-lg-3'))
    next_page_link = page.find('li', ('class', 'next'))

    print(next_page_link)
    list_link = []
    for part in result:
        postfix = part.find('a')['href']
        if str(postfix).find('catalogue') != -1:
            list_link.append(prs.urljoin(url_1, part.find('a')['href']))
        else:
            postfix = 'catalogue/'+ postfix
            list_link.append(prs.urljoin(url_1, postfix))
    try:
        for link in list_link:
            book_dict = {}
            res_good = requests.get(link)
            page_good = BeautifulSoup(res_good.content, 'html.parser')
            name = page_good.find('div', ('class', 'col-sm-6 product_main')).find('h1').text
            book_dict['name'] = name
            num_avail = page_good.find('p', ('class', 'instock availability')).text
            book_dict['num_avail'] = int(re.sub(r'[^\d.]+', '', num_avail))
            book_dict['price'] = page_good.find('div', ('class', 'col-sm-6 product_main')).find('p', ('class', 'price_color')).text
            describe  = page_good.find('div', ('class', 'sub-header')).next_siblings
            for item in describe:
                if str(item).find('<p>') != -1:
                    book_dict['describe'] = str(item)[3:-4]
            # all_book[name] = book_dict
            all_book.append(book_dict)
            time.sleep(1)
    except Exception as ex:
        print(ex)

    reply_str = json.dumps(all_book)
    with open('book.json', 'w+', encoding='UTF-8') as f:
        f.write(reply_str)


    if not next_page_link:
        break
    my_list = next_page_link.find('a')['href'].split('/')
    if 'catalogue' in my_list:
        url = prs.urljoin(url_1, next_page_link.find('a')['href'])
    else:
        prefix = url_1 + 'catalogue/'
        url = prs.urljoin(prefix, next_page_link.find('a')['href'])
    print(url)


