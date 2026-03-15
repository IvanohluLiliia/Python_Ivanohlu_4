"""
Модуль 3: Переклад тексту з використанням deep_translator.
Визначення мови з використанням langdetect.
"""

from deep_translator import GoogleTranslator
from langdetect import detect, detect_langs

# Таблиця мов deep_translator (GoogleTranslator) відповідає LANGUAGES з googletrans
LANGUAGES = GoogleTranslator().get_supported_languages(as_dict=True)
# LANGUAGES: {назва_мови: код_мови}


def _get_lang_code(lang: str) -> str:
    """Повертає код мови."""
    lang_lower = lang.strip().lower()
    # Якщо передано код → перевірити в значеннях
    if lang_lower in LANGUAGES.values():
        return lang_lower
    # Якщо передано назву → знайти код
    if lang_lower in LANGUAGES:
        return LANGUAGES[lang_lower]
    return lang_lower


def _get_lang_name(code: str) -> str:
    """Повертає назву мови за кодом."""
    code_lower = code.strip().lower()
    for name, c in LANGUAGES.items():
        if c == code_lower:
            return name
    return code_lower


def TransLate(text: str, scr: str, dest: str) -> str:
    """
    Перекладає текст з однієї мови на іншу.
    text – текст для перекладу
    scr  – назва або код мови джерела (або 'auto')
    dest – назва або код мови перекладу
    """
    try:
        src_code = 'auto' if scr.lower() == 'auto' else _get_lang_code(scr)
        dest_code = _get_lang_code(dest)
        translator = GoogleTranslator(source=src_code, target=dest_code)
        return translator.translate(text)
    except Exception as e:
        return f"Помилка перекладу: {e}"


def LangDetect(text: str, set: str = "all") -> str:
    """
    Визначає мову та коефіцієнт довіри для заданого тексту.
    set = "lang"       – тільки мова
    set = "confidence" – тільки коефіцієнт довіри
    set = "all"        – мова і коефіцієнт довіри
    """
    try:
        langs = detect_langs(text)
        top = langs[0]
        lang_code = top.lang
        confidence = round(top.prob, 4)
        lang_name = _get_lang_name(lang_code)

        if set == "lang":
            return f"{lang_name} ({lang_code})"
        elif set == "confidence":
            return str(confidence)
        else:
            return f"Мова: {lang_name} ({lang_code}), Коефіцієнт довіри: {confidence}"
    except Exception as e:
        return f"Помилка визначення мови: {e}"


def CodeLang(lang: str) -> str:
    """
    Якщо lang – назва мови, повертає її код.
    Якщо lang – код мови, повертає її назву.
    """
    lang_lower = lang.strip().lower()
    # Якщо назва → код
    if lang_lower in LANGUAGES:
        return LANGUAGES[lang_lower]
    # Якщо код → назва
    name = _get_lang_name(lang_lower)
    if name != lang_lower:
        return name
    return f"Помилка: мову '{lang}' не знайдено"


def LanguageList(out: str = "screen", text: str = None) -> str:
    """
    Виводить таблицю всіх підтримуваних мов та їх кодів.
    out = "screen" – вивести на екран
    out = "file"   – вивести у файл
    text           – текст для перекладу (необов'язково)
    """
    try:
        rows = []
        for name, code in LANGUAGES.items():
            if text:
                try:
                    translator = GoogleTranslator(source='auto', target=code)
                    translated = translator.translate(text)
                except Exception:
                    translated = "Помилка"
                rows.append((code, name, translated))
            else:
                rows.append((code, name))

        if text:
            col1_w = max(len("Код"), max(len(r[0]) for r in rows)) + 2
            col2_w = max(len("Мова"), max(len(r[1]) for r in rows)) + 2
            col3_w = max(len("Переклад"), max(len(r[2]) for r in rows)) + 2
            header = f"{'Код':<{col1_w}}{'Мова':<{col2_w}}{'Переклад':<{col3_w}}"
            separator = "-" * (col1_w + col2_w + col3_w)
            lines = [header, separator] + [
                f"{r[0]:<{col1_w}}{r[1]:<{col2_w}}{r[2]:<{col3_w}}" for r in rows
            ]
        else:
            col1_w = max(len("Код"), max(len(r[0]) for r in rows)) + 2
            col2_w = max(len("Мова"), max(len(r[1]) for r in rows)) + 2
            header = f"{'Код':<{col1_w}}{'Мова':<{col2_w}}"
            separator = "-" * (col1_w + col2_w)
            lines = [header, separator] + [
                f"{r[0]:<{col1_w}}{r[1]:<{col2_w}}" for r in rows
            ]

        table = "\n".join(lines)

        if out == "screen":
            print(table)
        elif out == "file":
            with open("languages_deeptr.txt", "w", encoding="utf-8") as f:
                f.write(table)
        else:
            return f"Помилка: невідомий параметр out='{out}'"

        return "Ok"
    except Exception as e:
        return f"Помилка: {e}"
