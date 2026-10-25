with open('Project/Config/DefaultGame.ini', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith('ProjectName='):
        new_lines.append('ProjectName=REVOLUTION (क्रांति)\n')
    elif line.strip() == '+DirectoriesToAlwaysCook=(Path="/Game/UI")':
        new_lines.append(line)
        new_lines.append('+DirectoriesToAlwaysCook=(Path="/Game/VFX")\n')
    else:
        new_lines.append(line)

with open('Project/Config/DefaultGame.ini', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Updated DefaultGame.ini successfully')
