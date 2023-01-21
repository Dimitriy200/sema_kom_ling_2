l1 = []
l2 = []
with open('PN_test.txt', 'r+') as file:
    # line = (file.readline())
    # line = int(line.replace('\n', ''))
    lines = file.readlines()
    line = lines[0]
    line = line.replace(f'\n', f'')
    lines.pop(0)
    # l2.clear()

    for i in range(len(lines)):
        l1.append(lines[i].replace(f'\n', f''))

    print(f'l1 = {l1}')

with open('NSL.txt', 'r+') as file:
    #print(*file)
    # l2.clear()

    # line = str((file.readline()))
    # line = int(line.replace('\n', ''))
    lines = file.readlines()
    line = lines[0]
    line = line.replace(f'\n', f'')
    lines.pop(0)
    # l2.clear()
    #lines[1] = lines[1].replace(f'\n', f'')
    #print(f'lines = {lines}')

    for i in range(len(lines)):
        l2.append(lines[i].replace(f'\n', f''))

    print(f'l2 = {l2}')
