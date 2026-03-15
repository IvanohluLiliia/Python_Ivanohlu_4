"""
gtrans3.py – демонстрація роботи функцій з модуля gtrans3_module (googletrans 3.1.0a0)
Для демонстрації потрібен Docker-контейнер з Python 3.12 або нижче.

Docker команди (виконати в терміналі):
    docker build -t ivanohlu -f Dockerfile.gtrans3 .
    docker run --name ivanohlu ivanohlu
"""

import sys

if sys.version_info >= (3, 13):
    print(
        "УВАГА: gtrans3_module використовує googletrans==3.1.0a0, "
        "яка несумісна з Python 3.13+.\n"
        "Запустіть цей файл у Docker-контейнері з Python 3.12 або нижче.\n"
        "Команди:\n"
        "  docker build -t ivanohlu -f Dockerfile.gtrans3 .\n"
        "  docker run --name ivanohlu ivanohlu"
    )
else:
    from ivanohlu_pkg import gtrans3_module as m3

    text_ua = (
        "Аж раптом, вельми несподівано для мене, Джобс зателефонував "
        "практично в новорічний вечір 2009 року."
    )

    print("=" * 60)
    print("Демонстрація gtrans3_module (googletrans 3.1.0a0)")
    print("=" * 60)

    print("\n1. TransLate (uk → en):")
    print(m3.TransLate(text_ua, "uk", "en"))

    print("\n2. TransLate (auto → fr):")
    print(m3.TransLate("Bonjour le monde", "auto", "en"))

    print("\n3. LangDetect (all):")
    print(m3.LangDetect(text_ua, "all"))

    print("\n4. LangDetect (lang):")
    print(m3.LangDetect(text_ua, "lang"))

    print("\n5. LangDetect (confidence):")
    print(m3.LangDetect(text_ua, "confidence"))

    print("\n6. CodeLang ('Ukrainian'):")
    print(m3.CodeLang("Ukrainian"))

    print("\n7. CodeLang ('uk'):")
    print(m3.CodeLang("uk"))

    print("\n8. LanguageList (screen) — результат Ok/Error:")
    print(m3.LanguageList("screen", "перевірка"))
