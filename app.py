import streamlit as st
import json
from streamlit_option_menu import option_menu
import datetime

class MovieApp:
    def __init__(self):
        self.page_index = 0  # Индекс текущей страницы

    # Функция для загрузки данных из JSON файла
    def load_movies_from_json(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            movies_data = json.load(file)
        return movies_data

    def filter_movies(self, movies, year=None, genre=None, title=None):
        if year:
            movies = [movie for movie in movies if movie.get('year') == year]
        if genre:
            movies = [movie for movie in movies if genre in movie.get('genres', '').split(', ')]
        if title:
            movies = [movie for movie in movies if title.lower() in movie.get('name', '').lower()]
        return movies

    def show_movies(self, movies_data):
        PLAYER_LINK = 'https://kinopoisk-watch-dsze5.ondigitalocean.app/player/'

        if movies_data:
            for i in range(0, len(movies_data), 6):  # Обработка по 6 фильмов за раз
                cols = st.columns(6)  # Используем шесть колонок в одной строке
                for col, movie in zip(cols, movies_data[i:i+6]):
                    try:
                        poster_image = movie['poster_url']
                        video_link = f"{PLAYER_LINK}?id={movie['id']}"  # Ссылка на видео просмотра
                        with col:
                            st.markdown(f"<a href='{video_link}' id='Movie_{i}'><img src='{poster_image}' width='100%'></a>", unsafe_allow_html=True)
                            st.caption(
                                f"###### {movie['name']}", 
                                help=(
                                    movie['description'] + '\n\n' + 
                                    str(f'Год: {movie['year']}') + ' \/ ' + 
                                    str(f'Рейтинг: {movie['rating']}') + ' \/ ' + 
                                    str(f'Страна: {movie['country']}') + ' \/ ' +                                     
                                    str(f'Продолжительность: {movie['duration']}') + ' \/ ' + 
                                    str(f'Бюджет: {movie['budget']}') + '\n\n' +
                                    movie['genres'] + '\n\n' + 
                                    movie['actors']
                                ),
                                unsafe_allow_html=True
                            )

                    except Exception as e:
                        st.error(f"Ошибка при отображении фильма: {e}")

    def run(self):
        st.set_page_config(layout="wide")  

        with st.sidebar:
            selected = option_menu(None, ["Фильмы", 'Сериалы', 'Мультики', 'Аниме'],
                                    icons=['bi bi-film', 'bi bi-tv', 'bi bi-gitlab', 'bi bi-fire'], menu_icon="bar-chart-fill", default_index=0, styles={
                    "container": {"padding": "5!important", "background-color":'black'},
                    "icon": {"color": "white", "font-size": "18px"},
                    "nav-link": {"color":"white", "font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                })
            
            # Поля ввода для фильтрации фильмов
            current_year = datetime.datetime.now().year
            year = st.selectbox("Выберите год", [None] + list(reversed(range(1900, current_year + 1))))
            genre = st.selectbox("Выберите жанр", [None] + ["драма", "комедия", "боевик", "триллер", "фантастика", "фэнтези", "ужасы", "детектив", "мультфильм"])
            title = st.text_input("Введите название фильма")

            # # Кнопки для пагинации
            # if st.button("← Назад"):
            #     if self.page_index > 0:
            #         self.page_index -= 1
            # if st.button("Вперед →"):
            #     self.page_index += 1

            # # Показать номер текущей страницы
            # st.text(f"Страница: {self.page_index + 1}")

        if selected == 'Фильмы':
            movies_data = self.load_movies_from_json("movies.json")
        elif selected == 'Сериалы':
            movies_data = self.load_movies_from_json("series.json")
        elif selected == 'Мультики':
            movies_data = self.load_movies_from_json("cartoons.json")
        elif selected == 'Аниме':
            movies_data = self.load_movies_from_json("anime.json")
        else:
            movies_data = self.load_movies_from_json("movies.json")

        # Применение фильтров
        filtered_movies = self.filter_movies(movies_data, year, genre, title)
        
        # Пагинация
        movies_per_page = 120
        start_index = self.page_index * movies_per_page
        end_index = start_index + movies_per_page
        movies_to_display = filtered_movies[start_index:end_index]

        # Отображение фильмов
        self.show_movies(movies_to_display)

if __name__ == "__main__":
    app = MovieApp()
    app.run()
