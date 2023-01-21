import re


def parser_sentence():
    # //////////////// ФУНКЦИИ ////////////////

    def contains_word(s, w):
        return (' ' + w + ' ') in (' ' + s + ' ')

    # //////////////// КОД ////////////////

    list_name = []

    with open('List_Name.txt', 'r+') as List_Name:
        list1 = List_Name.readlines()

        for i in range(len(list1)):
            list_name.append(list1[i].replace(f'\n', f''))

        with open('input.txt', 'r+') as input:
            input_text = input.read()
            input_text = input_text.replace(f'\n', f'')
            # print(input_text)
            output_text = []

            with open('PS_out.txt', 'w+') as output:
                for count_list_name in range(len(list_name)):
                    mid_text = input_text

                    mid_text = mid_text.replace(f'. ', f'.\n')
                    mid_text = mid_text.replace(f'.', f'.\n')

                    for i in range(len(list_name)):

                        with open('PSM.txt', 'w+') as mid:

                            mid.write(f'{mid_text}')

                            pattern = f"\.?(?P<sentence>.*?{list_name[count_list_name]}.*?)\."
                            match = re.search(pattern, mid_text)

                            if match is not None:
                                a = match.group("sentence")

                                mid_text = mid_text.replace(f'{a}', '')
                                # print(f'input_text = {input_text}')
                                # print(f'a = {a}\n')
                                output_text.append(f'{a}\n')
                                # print(f'mid = {mid_text}\n')

                # запись в выходной файлик и удаление лишних табуляций
                # print(f'len = {len(output_text)}')

                if len(output_text) == 0:  # если не найдено совпадений то запись не происходит
                    print('Совпадений не найдено')
                else:
                    for x in output_text:
                        if output_text.count(x) > 1:
                            output_text.remove(x)
                    print(output_text)  # [1, 2, 3, 4]

                    if output_text[-1][-1] == '\n':  # удаление лишних табуляций
                        # print('need delete \\n')
                        output_text[-1] = output_text[-1].replace(f'\n', f'')

                    for i in range(len(output_text)):
                        # запись в файлик
                        output.write(f'{output_text[i]}')


# parser_sentence()
