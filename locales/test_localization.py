import i18n
import yaml # Убедимся, что он установлен и импортируется

# 1. Укажите точный путь к папке, где лежат ваши .yml файлы
# Например, если они лежат в папке 'locales', то путь будет 'locales'
PATH_TO_LOCALES = '/Users/nick/AnimeGame_Project/locales'

# 2. Настраиваем i18n точно так же, как в вашем localization.py
i18n.load_path.append(PATH_TO_LOCALES)
i18n.set('filename_format', '{locale}.{format}')
i18n.set('file_format', 'yaml')

# 3. Проводим тесты
print("--- Тест для русского языка (ru) ---")
test_key_ru = 'main_menu_title'
translation_ru = i18n.t(test_key_ru, locale='ru')
print(f"Ключ: '{test_key_ru}', Результат: '{translation_ru}'")
# Проверим, равен ли результат ключу
if test_key_ru == translation_ru:
    print(">>> ОШИБКА: Перевод не найден, функция вернула ключ.")
else:
    print(">>> УСПЕХ: Перевод найден!")

print("\n" + "="*20 + "\n")

print("--- Тест для английского языка (en) ---")
test_key_en = 'main_menu_title'
translation_en = i18n.t(test_key_en, locale='en')
print(f"Ключ: '{test_key_en}', Результат: '{translation_en}'")
# Проверим, равен ли результат ключу
if test_key_en == translation_en:
    print(">>> ОШИБКА: Перевод не найден, функция вернула ключ.")
else:
    print(">>> УСПЕХ: Перевод найден!")