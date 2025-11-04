import os
import json



translations = {}

def load_translations():
        # 1. Получаем абсолютный путь к текущему файлу (localization.py)
    current_file_path = os.path.abspath(__file__)

    # 2. Получаем путь к папке, в которой лежит этот файл
    current_dir_path = os.path.dirname(current_file_path)

    # 3. "Приклеиваем" к пути нашей папки имя папки с переводами
    locales_dir_path = os.path.join(current_dir_path, 'locales')

    # Теперь в переменной locales_dir_path лежит надежный и всегда правильный путь к папке locales
    all_files_in_locales = os.listdir(locales_dir_path)
    for file in all_files_in_locales:
        if file[-5:] == '.json':
            translations[file[:-5]] = json.load(file_object)