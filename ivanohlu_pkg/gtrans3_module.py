"""
Модуль 2: Переклад тексту з використанням googletrans==3.1.0a0
Перевірка версії Python: якщо >= 3.13 – виводити повідомлення про несумісність.
"""

import sys

if sys.version_info >= (3, 13):
    print(
        "УВАГА: googletrans==3.1.0a0 не підтримує Python 3.13 і вище. "
        "Використовуйте модуль gtrans4_module (googletrans 4.x) або deeptr_module."
    )

try:
    from googletrans import Translator, LANGUAGES
    _AVAILABLE = True
except ImportError:
    _AVAILABLE = False


def _check_available():
    if not _AVAILABLE:
        raise RuntimeError("googletrans 3.1.0a0 не встановлено або не сумісне з поточною версією Python.")


def _get_lang_code(lang: str) -> str:
    lang_lower = lang.strip().lower()
    if lang_lower in LANGUAGES:
        return lang_lower
    for code, name in LANGUAGES.items():
        if name.lower() == lang_lower:
            return code
    return lang_lower


def TransLate(text: str, scr: str, dest: str) -> str:
    """
    Перекладає текст з однієї мови на іншу.
    text – текст для перекладу
    scr  – назва або код мови джерела (або 'auto')
    dest – назва або код мови перекладу
    """
    try:
        _check_available()
        src_code = 'auto' if scr.lower() == 'auto' else _get_lang_code(scr)
        dest_code = _get_lang_code(dest)
        translator = Translator()
        result = translator.translate(text, src=src_code, dest=dest_code)
        return result.text
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
        _check_available()
        translator = Translator()
        detected = translator.detect(text)
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


def CodeLang(lang: str) -> str:
    """
    Якщо lang – назва мови, повертає її код.
    Якщо lang – код мови, повертає її назву.
    """
    try:
        _check_available()
        lang_lower = lang.strip().lower()
        if lang_lower in LANGUAGES:
            return LANGUAGES[lang_lower]
        for code, name in LANGUAGES.items():
            if name.lower() == lang_lower:
                return code
        return f"Помилка: мову '{lang}' не знайдено"
    except Exception as e:
        return f"Помилка: {e}"


def LanguageList(out: str = "screen", text: str = None) -> str:
    """
    Виводить таблицю всіх підтримуваних мов та їх кодів.
    out = "screen" – вивести на екран
    out = "file"   – вивести у файл
    text           – текст для перекладу (необов'язково)
    """
    try:
        _check_available()
        translator = Translator() if text else None
        rows = []

        for code, name in LANGUAGES.items():
            if text:
                try:
                    result = translator.translate(text, dest=code)
                    translated = result.text
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
            with open("languages_gtrans3.txt", "w", encoding="utf-8") as f:
                f.write(table)
        else:
            return f"Помилка: невідомий параметр out='{out}'"

        return "Ok"
    except Exception as e:
        return f"Помилка: {e}"
