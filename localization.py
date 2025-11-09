# localization.py — универсальный и детализированный отладочный загрузчик локалей
import i18n
import os
import yaml

# --- DEBUG: место для вывода (можно заменить на логгер) ---
def _dbg(*args):
    print("[localization]", *args)

# 1) Путь к папке с переводами (относительно этого файла)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOCALES_DIR = os.path.join(CURRENT_DIR, "locales")

_dbg("CURRENT_DIR =", CURRENT_DIR)
_dbg("LOCALES_DIR =", LOCALES_DIR)
_dbg("Exists LOCALES_DIR?", os.path.exists(LOCALES_DIR))

# --- Настройка python-i18n (безопасно дополняем путь) ---
if LOCALES_DIR not in i18n.load_path:
    i18n.load_path.append(LOCALES_DIR)
_dbg("i18n.load_path =", i18n.load_path)

# Настройки
i18n.set('fallback', 'en')
i18n.set('file_format', 'yaml')
i18n.set('placeholder_delimiter', '{')

# --- Вспомогательные функции для отладки и fallback'а ---

# Попробуем прочитать файл YAML вручную (плоская структура или с корневым языком)
def _load_yaml_manual(lang):
    path = os.path.join(LOCALES_DIR, f"{lang}.yaml")
    _dbg("Manual load path:", path, "exists?", os.path.exists(path))
    if not os.path.exists(path):
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
            _dbg(f"Manual loaded keys for {lang}:", list(data.keys())[:20])
            return data
    except Exception as e:
        _dbg("YAML load error:", e)
        return {}

# Кеш для ручной подгрузки
_manual_cache = {}

# --- Основная функция ---
def get_string(language: str, key: str, **kwargs) -> str:
    """
    Универсальная функция получения локализованной строки.
    1) Пробует i18n.t("{lang}.{key}")
    2) Пробует i18n.t(key, locale=lang)
    3) Фоллбек: вручную загружает locales/{lang}.yaml и ищет ключ (поддерживает
       как плоскую структуру, так и вложенную {lang: {...}}).
    В логах видно, какой вариант сработал.
    """
    # 1) Попытка: ключ с префиксом языка (в случае, если YAML имеет корень 'en:')
    prefixed = f"{language}.{key}"
    try:
        res = i18n.t(prefixed, **kwargs)
        # python-i18n возвращает сам ключ, если не найден, поэтому сравним
        if res and res != prefixed:
            _dbg("Found via prefixed i18n.t ->", prefixed)
            return res
    except Exception as e:
        _dbg("i18n.t(prefixed) error:", e)

    # 2) Попытка: i18n.t(key, locale=language)
    try:
        res2 = i18n.t(key, locale=language, **kwargs)
        if res2 and res2 != key:
            _dbg("Found via i18n.t(key, locale=...) ->", key, "locale=", language)
            return res2
    except Exception as e:
        _dbg("i18n.t(key, locale=...) error:", e)

    # 3) Ручная загрузка YAML (fallback)
    if language not in _manual_cache:
        _manual_cache[language] = _load_yaml_manual(language)

    manual_data = _manual_cache.get(language, {})

    # Если в файле есть корень (например en: { main_menu_title: ... })
    if isinstance(manual_data, dict) and language in manual_data:
        val = manual_data.get(language, {}).get(key)
        if val:
            _dbg("Found via manual YAML under root (lang->key)")
            try:
                return val.format(**kwargs) if kwargs else val
            except Exception as e:
                _dbg("Format error:", e)
                return val

    # Если файл плоский: { main_menu_title: ... }
    val2 = manual_data.get(key)
    if val2:
        _dbg("Found via manual YAML flat structure")
        try:
            return val2.format(**kwargs) if kwargs else val2
        except Exception as e:
            _dbg("Format error:", e)
            return val2

    # Ничего не найдено — логируем и возвращаем ключ (поведение прежнее)
    _dbg(f"Translation NOT FOUND for lang='{language}', key='{key}'. Returning key.")
    return key