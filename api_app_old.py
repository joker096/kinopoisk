# pip install streamlit python-dotenv kinopoisk_dev requests
# https://github.com/odi1n/kinopoisk_dev

import os
import requests
import streamlit as st
import datetime

# Загрузка переменных окружения
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")
PLAYER_LINK = 'https://kinopoisk-watch-dsze5.ondigitalocean.app/player/'

# Определение доступных жанров вручную
GENRES = ["драма", "комедия", "боевик", "триллер", "фантастика", "фэнтези", "ужасы", "детектив", "мультфильм"]

@st.experimental_fragment
def fetch_movies(page=1, year=None, genre=None, rating=None, country=None):
    url = "https://api.kinopoisk.dev/v1.4/movie"
    headers = {
        "X-API-KEY": TOKEN
    }
    params = {"page": page}
    
    # Применяем фильтры
    if year:
        params["year"] = year
    if genre:
        params["genres.name"] = genre
    if rating:
        params["rating.imdb"] = rating
    if country:
        params["releaseYears.country"] = country
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Ошибка при получении данных: {response.status_code} - {response.text}")
        return None

def main():
    st.set_page_config(layout="wide")  # Устанавливаем настройки для отображения приложения на всю ширину

    st.title("Фильмы Kinopoisk")

    # Поля ввода для фильтрации фильмов
    current_year = datetime.datetime.now().year
    year = st.selectbox("Выберите год", list(reversed(range(1900, current_year + 1))))
    genre = st.selectbox("Выберите жанр", GENRES)
    rating = st.slider("Выберите рейтинг", 1, 10, (5, 10))
    country = st.text_input("Введите страну", "")

    page = st.number_input("Номер страницы", value=1, min_value=1, step=1)

    # Получение данных из API
    if st.button("Получить фильмы"):
        movies_data = fetch_movies(page, year, genre, f"{rating[0]}-{rating[1]}", country)

        # Отображение полученных данных
        if movies_data and "docs" in movies_data:
            # Разделение доступной ширины на 6 столбцов
            cols = st.columns(6)
            for movie, col in zip(movies_data["docs"], cols):
                if 'poster' in movie and movie['poster'] and 'description' in movie and movie['description']:  # Проверка наличия постера и описания
                    # Отображение информации о фильме
                    try:
                        poster_image = movie['poster']['url'] + "?width=100"  # Используем миниатюры
                        with col:
                            st.image(poster_image, use_column_width='auto', output_format='JPEG', clamp=True)
                            with st.expander(f"{movie['name']}"):
                                st.write(movie['description'])
                            link = f"{PLAYER_LINK}?id={movie['id']}"
                            st.markdown(f"[Смотреть {movie['name']}]({link})")
                    except Exception as e:
                        st.error(f"Ошибка при отображении фильма: {e}")
                else:
                    pass  # Не выводим ничего, если нет постера или описания

        else:
            st.write("Нет данных для отображения.")


if __name__ == "__main__":
    main()
