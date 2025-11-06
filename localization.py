# localization.py

import i18n
import os

# --- НАСТРОЙКА БИБЛИОТЕКИ (делается один раз) ---

# 1. Получаем абсолютный путь к папке с переводами ('locales')
current_dir_path = os.path.dirname(os.path.abspath(__file__))
locales_dir_path = os.path.join(current_dir_path, 'locales')

# 2. Указываем библиотеке, где искать наши файлы с переводами
i18n.load_path.append(locales_dir_path)

# 3. Указываем, какой язык использовать, если запрошенный не найден
i18n.set('fallback', 'en')

# 4. Указываем, какой формат файлов мы используем (YAML)
i18n.set('file_format', 'yaml')



# --- НАША ЕДИНСТВЕННАЯ ФУНКЦИЯ-ПОМОЩНИК ---

def get_string(lang,key, **kwargs):
  """
  Получает строку перевода для указанного языка и ключа.
  **kwargs используются для подстановки плейсхолдеров, например:
  get_string('ru', 'balance_text', balance=100)
  """
  # Мы просто "пробрасываем" запрос в библиотеку i18n
  i18n.set('locale', lang)
  return i18n.t(key, **kwargs)