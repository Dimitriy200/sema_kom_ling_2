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
global_link = []
# list1 = ['Название', 'Текст', 'Дата', 'Ссылка']

try:
    connection = sql.connect(host="localhost", user="root", password="", database="news")
    print('YES!')
except:
    print('NO!')
cursor = connection.cursor()
QUERY = 'SELECT name, description, date, ref FROM news'
QUERY_sentence = 'SELECT sentence, tone, link FROM sentence_tone'
# QUERY_relate = 'SELECT name, description, date, ref FROM news where ref LIKE \'https://riac34.ru/news/142612/\''


def vivod(ref):
    viv = f'SELECT name, description, date, ref ' \
          f'FROM news ' \
          f'where ref={ref}'
    try:
        cursor.execute(viv)
        print("sel es!")

        return viv
    except:
        print("sel not!")

    connection.commit()
    #return df3


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


def salam():
    return


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

# Дамп связи
# cursor.execute(QUERY_relate)
# result3 = pd.DataFrame(cursor.fetchall())
# print(result3)
# f = open('dbdump03.csv', 'w+')
# #result3.to_csv('dbdump03.csv', sep=',', encoding='UTF-8', mode='a', header=None, index=False)
# f.write(f'{vivod(global_link)}')
# df3 = pd.read_csv('dbdump03.csv')#vivod(global_link)
# print(result3)

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

    dash_table.DataTable(df2.to_dict('records'), [{"name": i, "id": i} for i in df2.columns], id='tbl2', page_size=10,
                         style_cell={
                             'whiteSpace': 'normal', 'overflowX': 'auto', 'maxWidth': '180px'
                         }),
    # dbc.Label('Связь', style={
    #     'textAlign': 'center', 'color': '#44944A', 'fontSize': '32px'
    # }),
    # dash_table.DataTable(df3.to_dict('records'), [{"name": i, "id": i} for i in df3.columns], id='tbl3', page_size=10,
    #                      style_cell={
    #                          'whiteSpace': 'normal', 'overflowX': 'auto', 'maxWidth': '180px'
    #                      }),
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
