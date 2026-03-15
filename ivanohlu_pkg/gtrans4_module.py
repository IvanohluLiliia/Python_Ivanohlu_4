"""
Модуль 1: Переклад тексту з використанням googletrans==4.0.0-rc.1 (4.x)
Асинхронні функції для Python 3.13+
"""

import asyncio
from googletrans import Translator, LANGUAGES


def _get_lang_code(lang: str) -> str:
    """Повертає код мови за назвою або сам код, якщо передано код."""
    lang_lower = lang.strip().lower()
    # Перевірити чи це вже код
    if lang_lower in LANGUAGES:
        return lang_lower
    # Шукати за назвою
    for code, name in LANGUAGES.items():
        if name.lower() == lang_lower:
            return code
    return lang_lower  # повернути як є (може бути 'auto')


async def TransLate(text: str, scr: str, dest: str) -> str:
    """
    Перекладає текст з однієї мови на іншу.
    text – текст для перекладу
    scr  – назва або код мови джерела (або 'auto')
    dest – назва або код мови перекладу
    """
    try:
        src_code = 'auto' if scr.lower() == 'auto' else _get_lang_code(scr)
        dest_code = _get_lang_code(dest)
        translator = Translator()
        result = await translator.translate(text, src=src_code, dest=dest_code)
        return result.text
    except Exception as e:
        return f"Помилка перекладу: {e}"


async def LangDetect(text: str, set: str = "all") -> str:
    """
    Визначає мову та коефіцієнт довіри для заданого тексту.
    set = "lang"       – тільки мова
    set = "confidence" – тільки коефіцієнт довіри
    set = "all"        – мова і коефіцієнт довіри
    """
    try:
        translator = Translator()
        detected = await translator.detect(text)
        lang_name = LANGUAGES.get(detected.lang, detected.lang)
        confidence = detected.confidence

        if set == "lang":
            return f"{lang_name} ({detected.lang})"
        elif set == "confidence":
            return str(confidence)
        else:
            return f"Мова: {lang_name} ({detected.lang}), Коефіцієнт довіри: {confidence}"
    except Exception as e:
        return f"Помилка визначення мови: {e}"


async def CodeLang(lang: str) -> str:
    """
    Якщо lang – назва мови, повертає її код.
    Якщо lang – код мови, повертає її назву.
    """
    lang_lower = lang.strip().lower()
    # Якщо код → назва
    if lang_lower in LANGUAGES:
        return LANGUAGES[lang_lower]
    # Якщо назва → код
    for code, name in LANGUAGES.items():
        if name.lower() == lang_lower:
            return code
    return f"Помилка: мову '{lang}' не знайдено"


async def LanguageList(out: str = "screen", text: str = None) -> str:
    """
    Виводить таблицю всіх підтримуваних мов та їх кодів.
    out = "screen" – вивести на екран
    out = "file"   – вивести у файл languages.txt
    text           – текст для перекладу (якщо вказано, додати колонку з перекладом)
    """
    try:
        translator = Translator() if text else None
        rows = []

        for code, name in LANGUAGES.items():
            if text:
                try:
                    result = await translator.translate(text, dest=code)
                    translated = result.text
                except Exception:
                    translated = "Помилка"
                rows.append((code, name, translated))
            else:
                rows.append((code, name))

        # Форматування таблиці
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
            with open("languages_gtrans4.txt", "w", encoding="utf-8") as f:
                f.write(table)
        else:
            return f"Помилка: невідомий параметр out='{out}'"

        return "Ok"
    except Exception as e:
        return f"Помилка: {e}"


# Синхронні обгортки для зручного виклику
def translate_sync(text: str, scr: str, dest: str) -> str:
    return asyncio.run(TransLate(text, scr, dest))


def lang_detect_sync(text: str, set: str = "all") -> str:
    return asyncio.run(LangDetect(text, set))


def code_lang_sync(lang: str) -> str:
    return asyncio.run(CodeLang(lang))


def language_list_sync(out: str = "screen", text: str = None) -> str:
    return asyncio.run(LanguageList(out, text))
