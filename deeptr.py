"""
deeptr.py – демонстрація роботи функцій з модуля deeptr_module (deep_translator + langdetect)
"""

from ivanohlu_pkg import deeptr_module as dt

text_ua = (
    "Аж раптом, вельми несподівано для мене, Джобс зателефонував "
    "практично в новорічний вечір 2009 року. Він саме був удома в "
    "Пало-Альто лише зі своєю сестрою, письменницею Моною Сімпсон."
)

print("=" * 60)
print("Демонстрація deeptr_module (deep_translator + langdetect)")
print("=" * 60)

print("\n1. TransLate (auto → en):")
print(dt.TransLate(text_ua, "auto", "en"))

print("\n2. TransLate (auto → de):")
print(dt.TransLate(text_ua, "auto", "de"))

print("\n3. TransLate (auto → fr):")
print(dt.TransLate("Hello world", "auto", "french"))

print("\n4. LangDetect (all):")
print(dt.LangDetect(text_ua, "all"))

print("\n5. LangDetect (lang):")
print(dt.LangDetect(text_ua, "lang"))

print("\n6. LangDetect (confidence):")
print(dt.LangDetect(text_ua, "confidence"))

print("\n7. CodeLang ('ukrainian'):")
print(dt.CodeLang("ukrainian"))

print("\n8. CodeLang ('uk'):")
print(dt.CodeLang("uk"))

print("\n9. CodeLang ('french'):")
print(dt.CodeLang("french"))

print("\n10. CodeLang ('de'):")
print(dt.CodeLang("de"))

print("\n11. LanguageList (file) → languages_deeptr.txt:")
print(dt.LanguageList("file"))

print("\n12. LanguageList (screen, з текстом 'Привіт') — перші рядки:")
# Щоб не перевантажувати вивід — демонструємо через file
print(dt.LanguageList("file", "Привіт"))
print("Результат збережено у languages_deeptr.txt")
