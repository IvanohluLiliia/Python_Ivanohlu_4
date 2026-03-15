"""
gtrans4.py – демонстрація роботи функцій з модуля gtrans4_module (googletrans 4.x, асинхронний)
"""

import asyncio
from ivanohlu_pkg import gtrans4_module as m4

async def main():
    print("=" * 60)
    print("Демонстрація gtrans4_module (googletrans 4.x, async)")
    print("=" * 60)

    # 1. TransLate
    text_ua = (
        "Аж раптом, вельми несподівано для мене, Джобс зателефонував "
        "практично в новорічний вечір 2009 року."
    )
    print("\n1. TransLate (uk → en):")
    result = await m4.TransLate(text_ua, "uk", "en")
    print(result)

    print("\n2. TransLate (auto → de):")
    result2 = await m4.TransLate("Hello, how are you?", "auto", "de")
    print(result2)

    # 2. LangDetect
    print("\n3. LangDetect (all):")
    print(await m4.LangDetect(text_ua, "all"))

    print("\n4. LangDetect (lang):")
    print(await m4.LangDetect(text_ua, "lang"))

    print("\n5. LangDetect (confidence):")
    print(await m4.LangDetect(text_ua, "confidence"))

    # 3. CodeLang
    print("\n6. CodeLang ('Ukrainian'):")
    print(await m4.CodeLang("Ukrainian"))

    print("\n7. CodeLang ('uk'):")
    print(await m4.CodeLang("uk"))

    print("\n8. CodeLang ('french'):")
    print(await m4.CodeLang("french"))

    # 4. LanguageList (перші 5 рядків на екран, без тексту перекладу)
    print("\n9. LanguageList (screen, без тексту) — перші 5 мов:")
    from googletrans import LANGUAGES
    items = list(LANGUAGES.items())[:5]
    col1_w, col2_w = 6, 20
    print(f"{'Код':<{col1_w}}{'Мова':<{col2_w}}")
    print("-" * (col1_w + col2_w))
    for code, name in items:
        print(f"{code:<{col1_w}}{name:<{col2_w}}")
    print("(повна таблиця: m4.language_list_sync('screen'))")

asyncio.run(main())
