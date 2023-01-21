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
QUERY_sentence = 'SELECT sentence, tone, link FROM sentence_tone'


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


info = html.find_all("div", class_="block-new")
for i in info:
    try:
        name = i.find(class_="caption").text.strip()
    except:
        name = ""

    try:
        heref = 'https://riac34.ru' + i.find(class_="caption").get("href").strip()
    except:
        heref = ""

    try:
        date = DateTransformation(i.find(class_="date").text).strip()
    except:
        date = ""

    try:
        text = DateTransformation(i.find(class_="desc").text).strip()
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
    # Query_show="SELECT * from news where name= '%s', description= '%s', date= '%s', ref= '%s'",(name, text, date,
    # heref)
    Query_show = "SELECT * from news where name='" + str(name) + "'and  description='" + str(
        text) + "'and date='" + str(date) + "'and ref='" + str(heref) + "'"
    # print(Query_show)
    count = cursor.execute(Query_show)
    # print(count)
    if count == 0:
        insert_not_tone(name, text, date, heref)

        # парсинг имен/работа с томита парсером
        sentence = main.search_name()
        sentence_ton = []

        # работа с тональностью
        for i in sentence:
            sentence_ton.append([i, tonalnost.tonality(i.replace(f'\n', f''))])

        for i in range(len(sentence_ton)):
            insert_sentence(sentence_ton[i][0], sentence_ton[i][1])


info = html.find_all("div", class_="new-block")
for i in info:
    try:
        name = i.find(class_="caption").text.strip()
        # print(name)
    except:
        name = ""

    try:
        heref = 'https://riac34.ru' + i.find(class_="caption").get("href").strip()
        # print(heref)
    except:
        heref = ""

    try:
        date = DateTransformation(i.find(class_="date").text).strip()
        # print(date)
    except:
        date = ""

    try:
        text = i.find(class_="desc").text.strip()
        # print(text)
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
            "Ссылка": heref}
    print(post)
    # Query_show="SELECT * from news where name= '%s', description= '%s', date= '%s', ref= '%s'",(name, text, date,
    # heref)
    Query_show = "SELECT * from news where name='" + str(name) + "'and  description='" + str(
        text) + "'and date='" + str(date) + "'and ref='" + str(heref) + "'"
    # print(Query_show)
    count = cursor.execute(Query_show)
    # print(count)
    if count == 0:
        insert_not_tone(name, text, date, heref)

        # парсинг имен/работа с томита парсером
        sentence = main.search_name()
        sentence_ton = []

        # работа с тональностью
        for i in sentence:
            sentence_ton.append([i, tonalnost.tonality(i.replace(f'\n', f''))])

        for i in range(len(sentence_ton)):
            insert_sentence(sentence_ton[i][0], sentence_ton[i][1])

info = html.find("div", class_="new-block-links").find_all("div", class_="item")
for i in info:
    try:
        name = i.find("a").text.strip()
        # print(name)
    except:
        name = ""

    try:
        heref = 'https://riac34.ru' + i.find("a").get("href").strip()
        # print(heref)
    except:
        heref = ""

    try:
        date = DateTransformation(i.find(class_="date").text).strip()
        # print(date)
    except:
        date = ""

    try:
        text = i.find(class_="desc").text.strip()
        # print(text)
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
            "Ссылка": heref}
    print(post)
    # Query_show="SELECT * from news where name= '%s', description= '%s', date= '%s', ref= '%s'",(name, text, date,
    # heref)
    Query_show = "SELECT * from news where name='" + str(name) + "'and  description='" + str(
        text) + "'and date='" + str(date) + "'and ref='" + str(heref) + "'"
    # print(Query_show)
    count = cursor.execute(Query_show)
    # print(count)
    if count == 0:
        insert_not_tone(name, text, date, heref)

        # парсинг имен/работа с томита парсером
        sentence = main.search_name()
        sentence_ton = []

        # работа с тональностью
        for i in sentence:
            sentence_ton.append([i, tonalnost.tonality(i.replace(f'\n', f''))])

        for i in range(len(sentence_ton)):
            insert_sentence(sentence_ton[i][0], sentence_ton[i][1])

info = html.find_all("div", class_="new-block-top")
for i in info:
    try:
        name = i.find(class_="title").text.strip()
        # print(name)
    except:
        name = ""

    try:
        heref = 'https://riac34.ru' + i.find("a").get("href").strip()
        # print(heref)
    except:
        heref = ""

    try:
        date = DateTransformation(i.find(class_="date").text).strip()
        # print(date)
    except:
        date = ""

    try:
        text = i.find(class_="desc").text.strip()
        # print(text)
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
            "Ссылка": heref}
    print(post)
    # Query_show="SELECT * from news where name= '%s', description= '%s', date= '%s', ref= '%s'",(name, text, date,
    # heref)
    Query_show = "SELECT * from news where name='" + str(name) + "'and  description='" + str(
        text) + "'and date='" + str(date) + "'and ref='" + str(heref) + "'"
    # print(Query_show)
    count = cursor.execute(Query_show)
    # print(count)
    if count == 0:
        insert_not_tone(name, text, date, heref)

        # парсинг имен/работа с томита парсером
        sentence = main.search_name()
        sentence_ton = []

        # работа с тональностью
        for i in sentence:
            sentence_ton.append([i, tonalnost.tonality(i.replace(f'\n', f''))])

        for i in range(len(sentence_ton)):
            insert_sentence(sentence_ton[i][0], sentence_ton[i][1])

info = html.find_all("div", class_="main-new")
for i in info:
    try:
        name = i.find(class_="title").text.strip()
        # print(name)
    except:
        name = ""

    try:
        heref = 'https://riac34.ru' + i.find("a").get("href").strip()
        # print(heref)
    except:
        heref = ""

    try:
        date = DateTransformation(i.find(class_="date").text).strip()
        # print(date)
    except:
        date = ""

    try:
        text = i.find(class_="desc").text.strip()
        # print(text)
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
            "Ссылка": heref}
    print(post)
    # Query_show="SELECT * from news where name= '%s', description= '%s', date= '%s', ref= '%s'",(name, text, date,
    # heref)
    Query_show = "SELECT * from news where name='" + str(name) + "'and  description='" + str(
        text) + "'and date='" + str(date) + "'and ref='" + str(heref) + "'"
    # print(Query_show)
    count = cursor.execute(Query_show)
    # print(count)
    if count == 0:
        insert_not_tone(name, text, date, heref)

        # парсинг имен/работа с томита парсером
        sentence = main.search_name()
        sentence_ton = []

        # работа с тональностью
        for i in sentence:
            sentence_ton.append([i, tonalnost.tonality(i.replace(f'\n', f''))])

        for i in range(len(sentence_ton)):
            insert_sentence(sentence_ton[i][0], sentence_ton[i][1])

# Дамп новостей
cursor.execute(QUERY)
result = pd.DataFrame(cursor.fetchall())
print(result)
f = open('dbdump01.csv', 'w')
result.to_csv('dbdump01.csv', sep=',', encoding='UTF-8', mode='a', header=None, index=False)

df = pd.read_csv('dbdump01.csv')

# Дамп предложений
cursor.execute(QUERY_sentence)
result2 = pd.DataFrame(cursor.fetchall())
print(result2)
f = open('dbdump02.csv', 'w')
result2.to_csv('dbdump02.csv', sep=',', encoding='UTF-8', mode='a', header=None, index=False)

df2 = pd.read_csv('dbdump02.csv')

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Label('Новости', style={
        'textAlign': 'center', 'color': '#44944A', 'fontSize': '32px'
    }),
    dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], id='tbl', page_size=10,
                         style_cell={
                             'whiteSpace': 'normal', 'overflowX': 'auto', 'maxWidth': '180px'
                         }),
    dbc.Label('Предложения', style={
        'textAlign': 'center', 'color': '#44944A', 'fontSize': '32px'
    }),

    dbc.Container(id='tbl_out', children=[]),

    dash_table.DataTable(df2.to_dict('records'), [{"name": i, "id": i} for i in df2.columns], id='tbl2', #page_size=10,
                         style_cell={
                             'whiteSpace': 'normal', 'overflowX': 'auto', 'maxWidth': '180px'
                         })
])  # ,style={'backgroundColor':'#2E2E2E'})

@app.callback(Output('tbl_out', 'children'),
              Input('tbl2', 'data'),
              Input('tbl2', 'active_cell'))
def display_output(rows, active_cell):
    # pruned_rows = []
    # for row in rows:
    #     # require that all elements in a row are specified
    #     # the pruning behavior that you need may be different than this
    #     if all([cell != '' for cell in row.values()]):
    #         pruned_rows.append(row)
    #
    #     print(row)
    # site2 = r.get("http://127.0.0.1:8050/")
    # html2 = BS(site2.content, "lxml")
    # pagelist = html2.find_all(class_="previous-next-container")
    # print(f'pagelist = {pagelist}')
    # page = int(pagelist[1].find(class_="current-page-shadow").text.strip())
    # print(page)
    if(active_cell):
        global_link = str(rows[active_cell['row']]['Ссылка'])

        # vivod(str(pruned_rows))
        # df3 = vivod(str(pruned_rows))

        viv = f"SELECT name, description, date, ref FROM news where ref LIKE'{global_link}'"
        ''

        cursor.execute(viv)
        # Дамп предложений
        result3 = pd.DataFrame(cursor.fetchall())
        print(result3)
        f = open('dbdump03.csv', 'w')
        result3.to_csv('dbdump03.csv', sep=',', encoding='UTF-8', mode='a', header=None, index=False)

        df3 = pd.read_csv('dbdump03.csv')
        children = [dash_table.DataTable(df3.to_dict('records'), [{"name": i, "id": i} for i in df3.columns], id='tbl3',
                                 page_size=10,
                                 style_cell={
                                     'whiteSpace': 'normal', 'overflowX': 'auto', 'maxWidth': '180px'
                                 })]
    return children if active_cell else "Click the table"


if __name__ == "__main__":
    app.run_server(debug=True)
    connection.commit()

    cursor.close()
    connection.close()
