import streamlit as st
import json
from streamlit_option_menu import option_menu
import datetime
import os

import base64
from pathlib import Path

class MovieApp:
    def __init__(self):
        self.page_index = 0  # Индекс текущей страницы

    # Функция для загрузки данных из JSON файла
    @st.experimental_fragment
    def load_movies_from_json(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            movies_data = json.load(file)
        return movies_data

    @st.experimental_fragment
    def filter_movies(self, movies, year=None, genre=None, title=None):
        if year:
            movies = [movie for movie in movies if movie.get('year') == year]
        if genre:
            movies = [movie for movie in movies if genre in movie.get('genres', '').split(', ')]
        if title:
            movies = [movie for movie in movies if title.lower() in movie.get('name', '').lower()]
        return movies

    @st.experimental_fragment
    def show_movies(self, movies_data):
        PLAYER_LINK = 'https://kinopoisk-watch-dsze5.ondigitalocean.app/player/'

        if movies_data:
            for i in range(0, len(movies_data), 6):  # Обработка по 6 фильмов за раз
                cols = st.columns(6)  # Используем шесть колонок в одной строке
                for col, movie in zip(cols, movies_data[i:i+6]):
                    try:
                        # Получение текущей рабочей директории
                        current_dir = os.getcwd()
                        # Определение пути к директории с изображениями относительно текущей рабочей директории
                        images_dir = os.path.join(current_dir, "images")
                        # Определение пути к изображению
                        # image_path = os.path.join(images_dir, f"{movie['id']}.jpg")
                        
                        # poster_image = movie['poster_url']
                        video_link = f"{PLAYER_LINK}?id={movie['id']}"  # Ссылка на видео просмотра
                        with col:                            
                            image_path = Path(__file__).with_name("images").joinpath(f"{movie['id']}.jpg").relative_to(Path.cwd())
                            # st.write(image_path)
                            # st.image(str(image_path))
                            # Чтение изображения в бинарном режиме
                            with open(image_path, "rb") as f:
                                image_bytes = f.read()

                            # Преобразование изображения в base64
                            image_base64 = base64.b64encode(image_bytes).decode()

                            # Формирование HTML-кода для встраивания изображения
                            html_code = f"<a href='{video_link}' id='{movie['id']}'><img src='data:image/jpeg;base64,{image_base64}' width='100%'></a>"

                            # Отображение изображения с помощью st.markdown
                            st.markdown(html_code, unsafe_allow_html=True)

                            # Ограничиваем длину описания до 300 символов
                            #movie['description'] = movie['description'][:300] + '...' if len(movie['description']) > 300 else movie['description']

                            # st.image(poster_image, use_column_width='auto', output_format='JPEG', clamp=True)
                            # st.markdown(f"<a href='{video_link}' id='Movie_{i}'><img src='{str(image_path)}' width='100%'></a>", unsafe_allow_html=True)
                            st.caption(
                                f"###### {movie['name']}",
                                help=(
                                    str(f'**{movie["description"]}**') + '\n\n' + 
                                    str(f'Год: {movie["year"]}') + ' / ' +
                                    str(f'Рейтинг: {movie["rating"]}') + ' / ' +
                                    str(f'Страна: {movie["country"]}') + ' / ' +
                                    (str(f'Продолжительность: {movie["duration"]}') + ' мин. / ' if movie["duration"] else '') +                                    
                                    str(f'{movie['genres']}') + '\n\n' + 
                                    str(f'Актёры: {movie["actors"]}') + '\n\n' +
                                    str(f'Режиссёр: {movie["directors"]}')
                                ),
                                unsafe_allow_html=True
                            )

                    except Exception as e:
                        st.error(f"Ошибка при отображении фильма: {e}")

    def run(self):
        st.set_page_config(layout="wide", page_title="Фильмы с Кинопоиск", page_icon="🎥")  

        st.markdown('###### Фильмотека', unsafe_allow_html=True)

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
            year = st.selectbox("", ["Выберите год"] + list(reversed(range(1950, current_year + 1))))
            if year == 'Выберите год':
                year = None

            genre = st.selectbox("", ["Выберите жанр"] + ["драма", "комедия", "боевик", "триллер", "фантастика", "фэнтези", "ужасы", "детектив", "мультфильм"])
            if genre == 'Выберите жанр':
                genre = None

            title = st.text_input("Поиск по названию")

            # # Кнопки для пагинации
            # cols = st.columns(5)
            # with cols[0]:
            #     if st.button("←"):
            #         if self.page_index > 0:
            #             self.page_index -= 1
            # with cols[4]:
            #     if st.button("→"):
            #         self.page_index += 1

            # # Показать номер текущей страницы
            # st.text(f"Страница: {self.page_index + 1}")

            # Кнопка для перехода на сайт "cvr.name" 
            st.link_button("Code & Description", "https://cvr.name/streamlit-powered-movie-app/", type="primary", use_container_width=True)
 
            # DONATE BUTTONS
            col1, col2 = st.columns(2)

            with col1:
                st.link_button("BTC", "https://pay.cryptomus.com/wallet/3b32a73a-5056-4367-998f-bca31573b8ba", type="secondary", use_container_width=True)
                st.link_button("LTC", "https://pay.cryptomus.com/wallet/9bda1c5d-5683-4c49-9c98-c6a2b2ae9498", type="secondary", use_container_width=True)
                st.link_button("DOGE", "https://pay.cryptomus.com/wallet/3e92f2ef-d69b-438b-a237-ff0d9b264ece", type="secondary", use_container_width=True)
                st.link_button("TRX", "https://pay.cryptomus.com/wallet/40e15597-f978-4ca3-9ceb-220503282004", type="secondary", use_container_width=True)
                st.link_button("DAI (BEP20)", "https://pay.cryptomus.com/wallet/494e3610-185c-48af-b053-5092f4ac88d9", type="secondary", use_container_width=True)

            with col2:
                st.link_button("USDT (TRC20)", "https://pay.cryptomus.com/wallet/c4003797-fc95-46ed-bedb-363f2243d09f", type="secondary", use_container_width=True)
                st.link_button("BNB", "https://pay.cryptomus.com/wallet/dac50c9d-a827-4c26-b689-3a44c8517c95", type="secondary", use_container_width=True)
                st.link_button("TON", "https://pay.cryptomus.com/wallet/0a76a081-7f74-4cc8-93c8-80e2b9c856d5", type="secondary", use_container_width=True)
                st.link_button("MATIC", "https://pay.cryptomus.com/wallet/03602ae6-c750-49de-ba09-7829bfb763f8", type="secondary", use_container_width=True)
                st.link_button("REGISTER", "https://cvr.name/aff-cryptomus", type="primary", use_container_width=True)

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
        movies_per_page = 240
        start_index = self.page_index * movies_per_page
        end_index = start_index + movies_per_page
        movies_to_display = filtered_movies[start_index:end_index]

        # Отображение фильмов
        self.show_movies(movies_to_display)

        # Back to Top
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

         # Define the target section's ID
        target_section_id = '742c3ac4'    

        # Generate and display the HTML content
        back_to_top_html = generate_back_to_top_html(target_section_id)
        st.markdown(back_to_top_html, unsafe_allow_html=True) 

if __name__ == "__main__":
    app = MovieApp()
    app.run()
