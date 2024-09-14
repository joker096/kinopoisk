import os
import requests
import json
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image, ImageFilter

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("TOKEN")

def save_image(image_url, movie_id, width=300):
    response = requests.get(image_url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content)).convert("RGB")
        aspect_ratio = float(image.height) / float(image.width)
        new_height = int(aspect_ratio * width)
        image = image.resize((width, new_height), Image.Resampling.LANCZOS)
        
        # Проверка на существование директории
        os.makedirs("images", exist_ok=True)
        
        output_path = os.path.join("images", f"{movie_id}.jpg")
        image.save(output_path)
        return output_path
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
        return None

def get_tapeop_id_from_api(kinopoisk_id):
    api_url = f'https://kinobox.tv/api/players?kinopoisk={kinopoisk_id}'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data:
            try:
                tapeop_url = data[2]['translations'][0]['iframeUrl']
                return tapeop_url
            except (IndexError, KeyError) as e:
                print(f"Error accessing translations for kinopoisk_id {kinopoisk_id}: {e}")
                tapeop_url = data[0]['translations'][0]['iframeUrl'] if data[0].get('translations') else None
                return tapeop_url
        else:            
            raise ValueError(f"Идентификатор Кинопоиска {kinopoisk_id} не найден в API")
    else:
        raise ValueError(f"Ошибка при получении идентификатора Tape Operator для ID {kinopoisk_id}: {response.status_code}")
    
def get_movie_details(movie_ids):
    # Если movie_ids - это список, обрабатываем каждый идентификатор
    if isinstance(movie_ids, list):
        return get_movie_details(movie_ids)
    # Если это одиночный id, обрабатываем как один фильм
    else:
        return get_movie_details([movie_ids])  # Обернем id в список

def get_movie_details(movie_id):
    url = f"https://api.kinopoisk.dev/v1.4/movie/{movie_id}"
    headers = {
        "X-API-KEY": TOKEN
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Данные для фильма с id {movie_id}: ", data)
        
        # Извлечение необходимых данных
        name = data.get('name', 'N/A')
        description = data.get('description', 'N/A')
        poster_url = data.get('poster', {}).get('url', 'N/A')
        poster_path = save_image(poster_url, movie_id, width=300) if poster_url != 'N/A' else None
        year = data.get('year', 'N/A')
        genres = ', '.join([genre['name'] for genre in data.get('genres', [])])
        rating = data.get('rating', {}).get('kp', 'N/A')
        actors = ', '.join([person['name'] for person in data.get('persons', []) if person['profession'] in ['актеры', 'actor'] and person['name']])
        directors = ', '.join([person['name'] for person in data.get('persons', []) if person['profession'] in ['режиссеры', 'director'] and person['name']])
        country = ', '.join([country['name'] for country in data.get('countries', [])])
        duration = data.get('movieLength', 'N/A')
        budget = data.get('budget', {}).get('value', 'N/A')

        # Получение TapeOp URL
        tapeop_url = get_tapeop_id_from_api(movie_id)
        
        return {
            "name": name,
            "description": description,
            "poster_url": poster_url,
            "poster_path": poster_path,
            "id": movie_id,
            "year": year,
            "genres": genres,
            "rating": rating,
            "actors": actors,
            "directors": directors,
            "country": country,
            "duration": duration,
            "budget": budget,
            "tapeop_url": tapeop_url
        }
    else:
        raise Exception(f"Ошибка при получении данных для фильма с id {movie_id}: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Для одного фильма
    movie_id = '70922'
    
    # Для нескольких фильмов
    # movie_ids = ['70922', '123456', '7891011']
    
    # Проверка для одного фильма
    movies_details = get_movie_details(movie_id)
    
    # Либо можно передать несколько ID
    # movies_details = get_movie_details(movie_ids)
    
    # Сохранение всех данных в JSON файл
    with open('movies_details.json', 'w', encoding='utf-8') as f:
        json.dump(movies_details, f, ensure_ascii=False, indent=4)

    # Вывод данных
    print(json.dumps(movies_details, ensure_ascii=False, indent=4))

