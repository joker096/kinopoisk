import json
from collections import OrderedDict

# список файлов, из которых нужно удалить дубликаты
filenames = ['cartoons.json', 'anime.json', 'movies.json']

# обрабатываем каждый файл отдельно
for filename in filenames:
    # читаем файл
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # создаем упорядоченный словарь для хранения уникальных фильмов по ключу 'id'
    unique_movies = OrderedDict()

    # добавляем уникальные фильмы в словарь
    for movie in data:
        unique_movies[movie['id']] = movie

    # сохраняем уникальные фильмы обратно в файл
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(list(unique_movies.values()), f, ensure_ascii=False, indent=4)
