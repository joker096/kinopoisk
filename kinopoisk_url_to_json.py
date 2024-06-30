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
        output_path = os.path.join("images", f"{movie_id}.jpg")
        image.save(output_path)
        return output_path
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
        return None


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
        if poster_url != 'N/A':
            poster_path = save_image(poster_url, movie_id, width=300)
        else:
            poster_path = None
        year = data.get('year', 'N/A')
        genres = ', '.join([genre['name'] for genre in data.get('genres', [])])
        rating = data.get('rating', {}).get('kp', 'N/A')
        actors = ', '.join([person['name'] for person in data.get('persons', []) if person['profession'] in ['актеры', 'actor']])
        directors = ', '.join([person['name'] for person in data.get('persons', []) if person['profession'] in ['режиссеры', 'director']])
        country = ', '.join([country['name'] for country in data.get('countries', [])])
        duration = data.get('movieLength', 'N/A')
        budget = data.get('budget', {}).get('value', 'N/A')
        
        return {
            "name": name,
            "description": description,
            "poster_url": poster_url,
            "id": movie_id,
            "year": year,
            "genres": genres,
            "rating": rating,
            "actors": actors,
            "directors": directors,
            "country": country,
            "duration": duration,
            "budget": budget
        }
    else:
        raise Exception(f"Ошибка при получении данных для фильма с id {movie_id}: {response.status_code} - {response.text}")

def get_movies_details(movie_ids):
    movies_details = []
    for movie_id in movie_ids:
        try:
            movie_details = get_movie_details(movie_id)
            movies_details.append(movie_details)
        except Exception as e:
            print(f"Error processing movie ID {movie_id}: {e}")
    return movies_details

if __name__ == "__main__":
    movie_ids = ['588', '1045172','450765','252156','195847','350','102474']
    
    movies_details = get_movies_details(movie_ids)
    
    with open('movies_details.json', 'w', encoding='utf-8') as f:
        json.dump(movies_details, f, ensure_ascii=False, indent=4)

    print(json.dumps(movies_details, ensure_ascii=False, indent=4))
