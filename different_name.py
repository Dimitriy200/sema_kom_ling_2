import functools
import requests as r
from bs4 import BeautifulSoup as BS
import re


def different_name():
    list_name = ''
    list1 = []
    list2 = []
    res = []

    with open('PN.txt', 'r') as file:
        lines = file.readlines()

        for i in range(len(lines)):
            list1.append(lines[i].replace(f'\n', f''))
            list_name = list_name + lines[i].replace(f'\n', f'.\n')

    with open('NSL.txt', 'r') as file:
        lines = file.readlines()

        for i in range(len(lines)):
            list2.append(lines[i].replace(f'\n', f''))

    for count_list_name in range(len(list2)):
        found_name = ''
        work_list_name = list_name

        for i in range(len(list2)):
            pattern = f"\.?(?P<sentence>.*?{list2[count_list_name]}.*?)\."
            match = re.search(pattern, work_list_name)

            if match is not None:
                found_name = match.group("sentence")

        if found_name != '':
            found = 1

            for j in range(len(res)):
                if res[j] == found_name:
                    found = 0

            if found:
                number = len(list2) / 2

                if count_list_name < number:
                    res.append(list2[count_list_name])
                    res.append(list2[(count_list_name + int(number))])
                else:
                    res.append(list2[(count_list_name - int(number))])
                    res.append(list2[count_list_name])

    #print(f'res = {res}')

    with open('List_Name.txt', 'w+') as file:

        for i in range(len(res)):
            if i == len(res) - 1:
                file.write(f'{res[i]}')
            else:
                file.write(f'{res[i]}\n')


# different_name()
