import functools
import requests as r
from bs4 import BeautifulSoup as BS
import re


def different_name():
    print(f'ФАЙЛ different_name')

    l1 = []
    l2 = []

    with open('PN_test.txt', 'r+') as file:
        lines = file.readlines()

        file.close()

        lines.pop(0)

        for i in range(len(lines)):
            l1.append(lines[i].replace(f'\n', f''))

    with open('NSL.txt', 'r+') as file:
        lines = file.readlines()

        file.close()

        lines.pop(0)

        for i in range(len(lines)):
            l2.append(lines[i].replace(f'\n', f''))

    l2.append('Бочаров Андрей Иванович')
    print(f'l1 содержит: {l1}')
    print(f'l2 содержит: {l2}')

    res = [x for x in l2 if x in l1]
    print(f'res = {res}')

    return res


different_name()
