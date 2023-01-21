import requests as r
from bs4 import BeautifulSoup as BS
from datetime import datetime, timedelta
import pymysql as sql
import csv
from dash import Dash, Input, Output, callback, dash_table
import pandas as pd
import dash_bootstrap_components as dbc
import main
import tonalnost


try:
    connection = sql.connect(host="localhost", user="root", password="", database="news")
    print('YES!')
except:
    print('NO!')
cursor = connection.cursor()
QUERY = 'SELECT name, description, date, ref FROM news'
QUERY_sentence = 'SELECT sentence, tone FROM sentence_tone'


def insert_sentence(sent, tone, ref):
    create_new = """
        INSERT INTO
          `sentence_tone` (`sentence`, `tone`, `link`)
        VALUES 
        ('""" + str(sent) + "' , '" + str(tone) + "' , '" + str(ref) + "') "
    print(create_new)

    try:
        cursor.execute(create_new)
        print("insert es!")
    except:
        print("insert not!")

    connection.commit()


def insert_not_tone(name, des, date, ref):
    create_new = """
    INSERT INTO
      `news` (`name`, `description`, `date`, `ref`)
    VALUES 
    ('""" + str(name) + "' , '" + str(des) + "' , '" + str(date) + "' , '" + str(ref) + "') "
    print(create_new)

    try:
        cursor.execute(create_new)
        print("insert es!")
    except:
        print("insert not!")

    connection.commit()


def DateTransformation(text):
    str1 = "сегодня в"
    str2 = "вчера в"
    if text.find(str1) > -1:
        text = text.replace(str1, datetime.today().strftime('%d %B,'))

    if text.find(str2) > -1:
        today = date.today()
        yesterday = today - timedelta(days=1)
        text = text.replace(str2, yesterday.strftime('%d %B,'))

    if text.find('January') > -1:
        text = text.replace('January', 'Января')

    if text.find('February ') > -1:
        text = text.replace('February', 'Февраля')

    if text.find('March') > -1:
        text = text.replace('March', 'Марта')

    if text.find('April') > -1:
        text = text.replace('April', 'Апреля')

    if text.find('May') > -1:
        text = text.replace('May', 'Мая')

    if text.find('June') > -1:
        text = text.replace('June', 'Июня')

    if text.find('July') > -1:
        text = text.replace('July', 'Июля')

    if text.find('August') > -1:
        text = text.replace('August', 'Августа')

    if text.find('September') > -1:
        text = text.replace('September', 'Сентября')

    if text.find('October') > -1:
        text = text.replace('October', 'Октября')

    if text.find('November') > -1:
        text = text.replace('November', 'Ноября')

    if text.find('December') > -1:
        text = text.replace('December', 'Декабря')

    return text


for item in range(142610, 152615, 1):

    site = r.get(f'https://riac34.ru/news/{item}/')
    html = BS(site.content, "lxml")

    i = html.find("div", class_="inner-new-content")

    try:
        name = i.find("h1").text.strip()
    except:
        name = ""

    try:
        heref = f'https://riac34.ru/news/{item}/'
    except:
        heref = ""

    try:
        date = DateTransformation(i.find(class_="news-attr").find(class_="date").text).strip()
    except:
        date = ""

    try:
        text = DateTransformation(i.find(class_="full-text").find("b").text).strip()
    except:
        text = ""

    # запись полученных данных во входной файл
    if text != '':
        name_text = name + '. ' + text
    else:
        name_text = name + '.'

    with open('input.txt', 'w+') as PS:
        PS.write(f'{name_text}')

    post = {"Название": name,
            "Текст": text,
            "Дата": date,
            "Ссылка": heref

            }

    print(post)

    Query_show = "SELECT * from news where name='" + str(name) + "'and  description='" + str(
        text) + "'and date='" + str(date) + "'and ref='" + str(heref) + "'"

    count = cursor.execute(Query_show)

    if count == 0:
        insert_not_tone(name, text, date, heref)

        # парсинг имен/работа с томита парсером
        sentence = main.search_name()
        sentence_ton = []

        # работа с тональностью

        for i in sentence:
            sentence_ton.append([i, tonalnost.tonality(i.replace(f'\n', f''))])

        for i in range(len(sentence_ton)):
            insert_sentence(sentence_ton[i][0], sentence_ton[i][1], f'{heref}')
