import requests as r
from bs4 import BeautifulSoup as BS


def parser_name1():
    list_name = []
    for item in range(0, 210, 20):
        site = r.get(f'https://global-volgograd.ru/person?offset={item}')

        html = BS(site.content, "lxml")

        info = html.find_all("div", class_="person-text")

        for i in info:
            name = i.find("div", class_="title").text.strip().title()
            list_name.append(name)

    with open('PN_test.txt', 'w+') as file:

        for j in range(len(list_name)):
            if j == len(list_name) - 1:
                file.write(f'{list_name[j]}')
            else:
                file.write(f'{list_name[j]}\n')
