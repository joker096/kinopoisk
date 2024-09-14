import json
import requests

# Функция для получения URL по кинопоиск ID
def get_tapeop_id_from_api(kinopoisk_id):
    api_url = f'https://kinobox.tv/api/players?kinopoisk={kinopoisk_id}'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data:
            try:
                tapeop_url = data[2]['translations'][0]['iframeUrl']
                return tapeop_url
            except IndexError:
                tapeop_url = data[0]['translations'][0]['iframeUrl']
                return tapeop_url
        else:            
            raise ValueError(f"Идентификатор Кинопоиска {kinopoisk_id} не найден в API")
    else:
        raise ValueError(f"Ошибка при получении идентификатора Tape Operator для ID {kinopoisk_id}")

# Чтение данных из JSON файла
with open('series.json', 'r', encoding='utf-8') as file:
    films = json.load(file)

# Добавление tapeop_url к каждому фильму
for film in films:
    try:
        tapeop_url = get_tapeop_id_from_api(film['id'])
        film['tapeop_url'] = tapeop_url
    except Exception as e:
        print(f"Ошибка для фильма '{film['name']}': {e}")

# Сохранение обновленных данных обратно в JSON файл
with open('updated_films.json', 'w', encoding='utf-8') as file:
    json.dump(films, file, ensure_ascii=False, indent=4)

print("Данные успешно обновлены и сохранены в updated_films.json")
