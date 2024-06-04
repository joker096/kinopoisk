# MovieApp

![MovieApp Screenshot](screenshot.png)

Это веб-приложение на Streamlit для просмотра информации о фильмах. Пользователь может фильтровать фильмы по году выпуска, жанру и названию. Пагинация обеспечивает удобную навигацию между страницами результатов.

## Установка

1. Установите необходимые зависимости, выполнив следующую команду:

```
pip install streamlit streamlit_option_menu
```
2. Склонируйте репозиторий:

```
git clone https://github.com/<ваш-логин>/MovieApp.git
cd MovieApp
```

3. Создайте виртуальную среду и активируйте ее:
```
python -m venv .venv
.\.venv\Scripts\activate  # Для Windows
source .venv/bin/activate  # Для MacOS/Linux
```

4. Использование:

Запустите приложение, введя следующую команду:

```
streamlit run app.py
```
5. Структура проекта:

app.py: Основной код приложения.
movies.json: JSON файл с данными о фильмах.
series.json, cartoons.json, anime.json: Дополнительные JSON файлы с данными о сериалах, мультфильмах и аниме соответственно.
screenshot.png: Скриншот приложения для демонстрации.
kinopoisk_url_to_json.py - вспомогательный скрипт, позволяющий получить данные из Кинопоиска по id фильмам в json формат.

demo: https://kinopoisk.streamlit.app/