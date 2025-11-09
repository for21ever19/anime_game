
import i18n
import os

# --- НАСТРОЙКА БИБЛИОТЕКИ (делается один раз) ---

# 1. Путь к папке с переводами ('locales')
current_dir_path = os.path.dirname(os.path.abspath(__file__))
locales_dir_path = os.path.join(current_dir_path, 'locales')

# 2. Указываем библиотеке, где искать наши YAML
i18n.load_path.append(locales_dir_path)

# 3. Язык по умолчанию, если не найден нужный
i18n.set('fallback', 'en')

# 4. Формат файлов
i18n.set('file_format', 'yaml')

# 5. Чтобы можно было подставлять {balance} и т.п.
i18n.set('placeholder_delimiter', '{')

# --- НАША ОСНОВНАЯ ФУНКЦИЯ ---
def get_string(language, key, **kwargs):
    try:
        # ⚠️ убери язык из ключа, т.к. теперь YAML без уровня 'en:'
        return i18n.t(key, locale=language, **kwargs)
    except Exception as e:
        print(f"[localization] Ошибка: {e}")
        return key