from xml.dom import minidom

dom = minidom.parse('output.xml.xml')

Name_Surname = dom.getElementsByTagName('Name_Surname')
Name_FirstName = dom.getElementsByTagName('Name_FirstName')

print(f"There are {len(Name_Surname)} Surname:")

for Name_Surname in Name_Surname:
    print(Name_Surname.attributes['val'].value)

print(f"There are {len(Name_FirstName)} FirstName:")

for Name_FirstName in Name_FirstName:
    print(Name_FirstName.attributes['val'].value)
