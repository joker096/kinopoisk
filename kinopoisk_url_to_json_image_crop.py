import os
import requests
import json
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("TOKEN")

def resize_image(image_url, new_width):
    response = requests.get(image_url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        aspect_ratio = image.width / image.height
        new_height = int(new_width / aspect_ratio)
        resized_image = image.resize((new_width, new_height))
        output_path = f"{os.path.splitext(os.path.basename(image_url))[0]}_resized.jpg"
        # resized_image.save(output_path)
        return output_path
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
        return image_url

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
            poster_url = resize_image(poster_url, 300)
        year = data.get('year', 'N/A')
        genres = ', '.join([genre['name'] for genre in data.get('genres', [])])
        rating = data.get('rating', {}).get('kp', 'N/A')
        actors = ', '.join([person['name'] for person in data.get('persons', []) if person['profession'] == 'актёр'])
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
    movie_ids = [
        "775276",
        # "685246",
        # "46483",
        # "279102",
        # "45319",
        # "775273",
        # "591929",
        # "920265",
        # "42326",
        # "432724",
        # "694051",
        # "842567",
        # "103734",
        # "45779",
        # "550910",
        # "79920",
        # "77164",
        # "988782",
        # "1009142",
        # "821008",
        # "38903",
        # "839650"
    ]
    
    movies_details = get_movies_details(movie_ids)
    
    with open('movies_details.json', 'w', encoding='utf-8') as f:
        json.dump(movies_details, f, ensure_ascii=False, indent=4)

    print(json.dumps(movies_details, ensure_ascii=False, indent=4))
