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

site = r.get("https://riac34.ru")
html = BS(site.content, "lxml")

try:
    connection = sql.connect(host="localhost", user="root", password="", database="news")
    print('YES!')
except:
    print('NO!')
cursor = connection.cursor()
QUERY = 'SELECT name, description, date, ref FROM news'
QUERY_sentence = 'SELECT sentence, tone FROM sentence_tone'


def insert_sentence(sent, tone):
    create_new = """
        INSERT INTO
          `sentence_tone` (`sentence`, `tone`)
        VALUES 
        ('""" + str(sent) + "' , '" + str(tone) + "') "
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



with open('dbdump01.csv', 'r') as file:
    #list=file.readlines()
    reader = csv.reader(file)
    list_sent=list(reader)


for i in range(len(list_sent)):

    if list_sent[i][1] != '':
        name_text = list_sent[i][0] + '. ' +  list_sent[i][1]
    else:
        name_text =  list_sent[i][0] + '.'

    with open('input.txt', 'w+') as PS:
        PS.write(f'{name_text}')

    sentence = main.search_name()

    sentence_ton = []
    for i in sentence:
        sentence_ton.append([i, tonalnost.tonality(i.replace(f'\n', f''))])

    for i in range(len(sentence_ton)):
        print(sentence_ton[i][0])
        print(sentence_ton[i][1])
        insert_sentence(sentence_ton[i][0], sentence_ton[i][1])

    #print(sentence_ton)








