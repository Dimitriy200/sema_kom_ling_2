import xml.etree.ElementTree as ET


def parser_attraction_xml_etree():
    root = ET.parse('attraction_output.xml').getroot()

    Name = []
    Object = []
    list1 = []
    list2 = []

    for type_tag in root.findall('document/facts/Attraction/Name'):
        char = (type_tag.get('val'))
        Name.append(char.title())

    for type_tag in root.findall('document/facts/Attraction/Object'):
        char = (type_tag.get('val'))
        Object.append(char.title())

    for i in range(len(Name)):
        try:
            list1.append(Name[i] + " " + Object[i])
            list2.append(Object[i] + " " + Name[i])
        except:
                list1.append(Name[i])
                list2.append(Name[i])

    with open('Attr.txt', 'w+') as file:

        for j in range(len(list1)):
            file.write(f'{list1[j]}\n')

        for j in range(len(list2)):
            if j == len(list2) - 1:
                file.write(f'{list2[j]}')
            else:
                file.write(f'{list2[j]}\n')


parser_attraction_xml_etree()
