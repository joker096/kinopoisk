import json

# Замените 'data.json' на имя вашего файла с данными
with open('series.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Извлечение всех значений 'id'
ids = [item['id'] for item in data]

# Печать списка 'id'
print(ids)

# Сохранение списка 'id' в файл
with open('ids.json', 'w', encoding='utf-8') as outfile:
    json.dump(ids, outfile, ensure_ascii=False, indent=4)
