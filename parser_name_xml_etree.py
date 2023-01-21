import xml.etree.ElementTree as ET


def parser_name_xml_etree():
    root = ET.parse('output.xml').getroot()

    Name_Surname = []
    Name_FirstName = []
    list1 = []
    list2 = []

    for type_tag in root.findall('document/facts/Person/Name_Surname'):
        char = (type_tag.get('val'))
        Name_Surname.append(char.title())

    for type_tag in root.findall('document/facts/Person/Name_FirstName'):
        char = (type_tag.get('val'))
        Name_FirstName.append(char.title())

    for i in range(len(Name_Surname)):
        try:
            list1.append(Name_Surname[i] + " " + Name_FirstName[i])
            list2.append(Name_FirstName[i] + " " + Name_Surname[i])
        except:
            print()

    with open('NSL.txt', 'w+') as file:

        for j in range(len(list1)):
            file.write(f'{list1[j]}\n')

        for j in range(len(list2)):
            if j == len(list2) - 1:
                file.write(f'{list2[j]}')
            else:
                file.write(f'{list2[j]}\n')


# parser_name_xml_etree()
