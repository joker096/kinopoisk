import os
import requests
import json
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("TOKEN")

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
    movie_ids = ['404900', '253245', '749374', '1227803', '502838', '685246', '4445150', '460586', '406148', '257376', '591929', '5378717', '915196', '1394131', '1197956', '681831', '4867607', '1032606']
    
    movies_details = get_movies_details(movie_ids)
    
    with open('movies_details.json', 'w', encoding='utf-8') as f:
        json.dump(movies_details, f, ensure_ascii=False, indent=4)

    print(json.dumps(movies_details, ensure_ascii=False, indent=4))
