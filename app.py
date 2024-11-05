import streamlit as st
import json
from streamlit_option_menu import option_menu
import datetime
import os
import base64
from pathlib import Path
import requests
import streamlit.components.v1 as components

class MovieApp:
    def __init__(self):
        self.page_index = 0  # Индекс текущей страницы

    @st.experimental_fragment
    def load_movies_from_json(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            movies_data = json.load(file)
        return movies_data

    @st.experimental_fragment
    def filter_movies(self, movies, year=None, genre=None, title=None, actor=None):
        if year:
            movies = [movie for movie in movies if movie.get("year") == year]
        if genre:
            movies = [movie for movie in movies if genre in movie.get("genres", "").split(", ")]
        if title:
            movies = [movie for movie in movies if title.lower() in movie.get("name", "").lower()]
        if actor:
            movies = [movie for movie in movies if actor.lower() in movie.get("actors", "").lower()]
        return movies

    @st.experimental_fragment
    def show_movies(self, movies_data):        
        if movies_data:
            for i in range(0, len(movies_data), 6):  # Обработка по 6 фильмов за раз
                cols = st.columns(6)  # Используем шесть колонок в одной строке
                for col, movie in zip(cols, movies_data[i:i+6]):
                    try:
                        current_dir = os.getcwd()
                        images_dir = os.path.join(current_dir, "images")
                        with col:
                            image_path = Path(__file__).with_name("images").joinpath(f"{movie['id']}.jpg").relative_to(Path.cwd())
                            with open(image_path, "rb") as f:
                                image_bytes = f.read()

                            image_base64 = base64.b64encode(image_bytes).decode()

                            html_code = f"<a href=\"{movie['tapeop_url']}\"><img src=\"data:image/jpeg;base64,{image_base64}\" width='100%'></a>"

                            st.markdown(html_code, unsafe_allow_html=True)

                            st.caption(
                                f"###### {movie['name']}",
                                help=(f"**{movie['description']}**" + "\n\n" +
                                      f"Год: {movie['year']}" + " / " +
                                      f"Рейтинг: {movie['rating']}" + " / " +
                                      f"Страна: {movie['country']}" + " / " +
                                      (f"Продолжительность: {movie['duration']}" + " мин. / " if movie["duration"] else "") +
                                      f"{movie['genres']}" + "\n\n" +
                                      f"Актёры: {movie['actors']}" + "\n\n" +
                                      f"Режиссёр: {movie['directors']}"
                                ),
                                unsafe_allow_html=True
                            )

                    except Exception as e:
                        st.error(f"Ошибка при отображении фильма: {e}")

    def run(self):
        st.set_page_config(layout="wide", page_title="Фильмы с Кинопоиск", page_icon="🎥")

        st.markdown("###### Фильмотека", unsafe_allow_html=True)

        with st.sidebar:
            selected = option_menu(None, ["Фильмы", "Сериалы", "Мультики", "Аниме"],
                                   icons=["bi bi-film", "bi bi-tv", "bi bi-gitlab", "bi bi-fire"],
                                   menu_icon="bar-chart-fill", default_index=0, styles={
                                       "container": {"padding": "5!important", "background-color": "black"},
                                       "icon": {"color": "white", "font-size": "18px"},
                                       "nav-link": {"color": "white", "font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                                       "nav-link-selected": {"background-color": "#02ab21"},
                                   })

            current_year = datetime.datetime.now().year
            year = st.selectbox("", ["Выберите год"] + list(reversed(range(1950, current_year + 1))))
            if year == "Выберите год":
                year = None

            genre = st.selectbox("", ["Выберите жанр"] + ["драма", "комедия", "боевик", "триллер", "фантастика", "фэнтези", "ужасы", "детектив", "мультфильм"])
            if genre == "Выберите жанр":
                genre = None

            title = st.text_input("Поиск по названию")
            actor = st.text_input("Поиск по актёру")  # Добавлено поле для поиска по актёру

            st.link_button("Code & Description", "https://cvr.name/streamlit-powered-movie-app/", type="primary", use_container_width=True)

            components.iframe("https://nowpayments.io/embeds/donation-widget?api_key=8Y7S20R-2AAMZRA-MH6Y1GY-PVKA9FV", height=623)

        if selected == "Фильмы":
            movies_data = self.load_movies_from_json("movies.json")
        elif selected == "Сериалы":
            movies_data = self.load_movies_from_json("series.json")
        elif selected == "Мультики":
            movies_data = self.load_movies_from_json("cartoons.json")
        elif selected == "Аниме":
            movies_data = self.load_movies_from_json("anime.json")
        else:
            movies_data = self.load_movies_from_json("movies.json")

        filtered_movies = self.filter_movies(movies_data, year, genre, title, actor)  # Передача actor в метод фильтрации

        movies_per_page = 240
        start_index = self.page_index * movies_per_page
        end_index = start_index + movies_per_page
        movies_to_display = filtered_movies[start_index:end_index]

        self.show_movies(movies_to_display)

        @st.experimental_fragment
        def generate_back_to_top_html(target_section_id):
            st.divider()
            return f'''
                <a style="text-decoration: none;" href="#{target_section_id}">
                    <div style="background-color: #00A6ED; color: white; padding: 10px 20px; border-radius: 5px; cursor: pointer; text-align: center;">
                        ⬆️
                    </div>
                </a>
            '''

        target_section_id = "742c3ac4"
        back_to_top_html = generate_back_to_top_html(target_section_id)
        st.markdown(back_to_top_html, unsafe_allow_html=True)

if __name__ == "__main__":
    app = MovieApp()
    app.run()
