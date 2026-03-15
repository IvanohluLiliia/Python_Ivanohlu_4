"""
filetr.py – програма для перекладу тексту з файлу згідно з конфігураційним файлом config.ini
"""

import os
import re
import importlib
import configparser

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")


def read_config(config_file: str) -> dict:
    """Читає конфігураційний файл."""
    config = configparser.ConfigParser()
    config.read(config_file, encoding="utf-8")
    section = "translation"
    return {
        "input_file": config.get(section, "input_file"),
        "dest_language": config.get(section, "dest_language"),
        "module": config.get(section, "module"),
        "output": config.get(section, "output"),
        "sentences_count": config.getint(section, "sentences_count"),
    }


def split_sentences(text: str) -> list:
    """Розбиває текст на речення."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if s.strip()]


def detect_language(text: str, module_name: str) -> str:
    """Визначає мову тексту за допомогою заданого модуля."""
    try:
        if module_name == "deeptr_module":
            mod = importlib.import_module(f"ivanohlu_pkg.{module_name}")
            return mod.LangDetect(text, "lang")
        elif module_name == "gtrans4_module":
            mod = importlib.import_module(f"ivanohlu_pkg.{module_name}")
            import asyncio
            return asyncio.run(mod.LangDetect(text, "lang"))
        else:
            mod = importlib.import_module(f"ivanohlu_pkg.{module_name}")
            return mod.LangDetect(text, "lang")
    except Exception as e:
        return f"Помилка: {e}"


def translate_text(text: str, dest: str, module_name: str) -> str:
    """Перекладає текст за допомогою заданого модуля."""
    try:
        if module_name == "gtrans4_module":
            mod = importlib.import_module(f"ivanohlu_pkg.{module_name}")
            import asyncio
            return asyncio.run(mod.TransLate(text, "auto", dest))
        else:
            mod = importlib.import_module(f"ivanohlu_pkg.{module_name}")
            return mod.TransLate(text, "auto", dest)
    except Exception as e:
        return f"Помилка перекладу: {e}"


def get_lang_name(code: str, module_name: str) -> str:
    """Повертає назву мови за кодом."""
    try:
        if module_name == "gtrans4_module":
            mod = importlib.import_module(f"ivanohlu_pkg.{module_name}")
            import asyncio
            return asyncio.run(mod.CodeLang(code))
        else:
            mod = importlib.import_module(f"ivanohlu_pkg.{module_name}")
            return mod.CodeLang(code)
    except Exception:
        return code


def main():
    # Читання конфігурації
    if not os.path.exists(CONFIG_FILE):
        print(f"Помилка: конфігураційний файл '{CONFIG_FILE}' не знайдено.")
        return

    try:
        cfg = read_config(CONFIG_FILE)
    except Exception as e:
        print(f"Помилка читання конфігурації: {e}")
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = cfg["input_file"]
    if not os.path.isabs(input_file):
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), input_file)
    if not os.path.isabs(input_file):
        input_file = os.path.join(script_dir, input_file)
    dest_lang = cfg["dest_language"]
    module_name = cfg["module"]
    output_mode = cfg["output"]
    sentences_count = cfg["sentences_count"]

    # === I. Інформація про файл ===
    if not os.path.exists(input_file):
        print(f"Помилка: файл '{input_file}' не знайдено.")
        return

    file_size = os.path.getsize(input_file)

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            full_text = f.read()
    except Exception as e:
        print(f"Помилка читання файлу: {e}")
        return

    char_count = len(full_text)
    all_sentences = split_sentences(full_text)
    sentence_count_total = len(all_sentences)
    detected_lang = detect_language(full_text[:500], module_name)

    print(f"\n{'='*60}")
    print(f"Файл:             {input_file}")
    print(f"Розмір:           {file_size} байт")
    print(f"Кількість символів: {char_count}")
    print(f"Кількість речень: {sentence_count_total}")
    print(f"Мова тексту:      {detected_lang}")
    print(f"{'='*60}\n")

    # === II. Читання та переклад ===
    selected_sentences = all_sentences[:sentences_count]
    text_to_translate = " ".join(selected_sentences)

    translated = translate_text(text_to_translate, dest_lang, module_name)
    lang_name = get_lang_name(dest_lang, module_name)

    # === IV/V. Виведення результату ===
    if output_mode == "screen":
        print(f"Мова перекладу: {lang_name} ({dest_lang})")
        print(f"Модуль:         {module_name}")
        print(f"\nПерекладений текст:\n{'-'*60}")
        print(translated)
        print(f"{'-'*60}")

    elif output_mode == "file":
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}_{dest_lang}{ext}"
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"Мова перекладу: {lang_name} ({dest_lang})\n")
                f.write(f"Модуль: {module_name}\n")
                f.write(f"{'-'*60}\n")
                f.write(translated)
            print("Ok")
        except Exception as e:
            print(f"Помилка запису файлу: {e}")
    else:
        print(f"Помилка: невідомий режим виведення '{output_mode}'.")


if __name__ == "__main__":
    main()
