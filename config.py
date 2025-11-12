# config.py
import os

# Определяем базовую директорию проекта.
# __file__ — это путь к текущему файлу (т.е. к config.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Теперь все остальные пути строим от этой базовой директории
IMAGES_DIR = os.path.join(BASE_DIR, 'images_processed')
FONTS_DIR = os.path.join(BASE_DIR, 'Fonts')
QUESTIONS_DIR = os.path.join(BASE_DIR, 'questions') # <-- Обратите внимание!