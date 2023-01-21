import requests as r
from bs4 import BeautifulSoup as BS


def parser_attraction():

    site = r.get('https://avolgograd.com/sights')
    html = BS(site.content, "lxml")
    list_attr = []


    info = html.find_all("div", class_="ta-210")

    for i in info:
        attr = i.find("div", class_="ta-211").text.strip().title()
        print(attr)
        list_attr.append(attr)

    with open('PA.txt', 'w+') as file:

        for j in range(len(list_attr)):
            if j == len(list_attr) - 1:
                file.write(f'{list_attr[j]}')
            else:
                file.write(f'{list_attr[j]}\n')


parser_attraction()
