#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Примеры использования библиотеки LangDefLib.
"""

from LangDefLib import LangDetector, detect_language


def basic_usage():
    """Базовое использование библиотеки."""
    print("\n=== Базовое использование ===")
    
    # Быстрое определение языка
    text_ru = "Это пример текста на русском языке. Он содержит особенности русского языка."
    result = detect_language(text_ru)
    print(f"Определен язык: {result['language']}, уверенность: {result['confidence']:.2f}")
    
    # Создание детектора с указанными языками
    detector = LangDetector(languages=['russian', 'ukrainian', 'english'])
    
    # Определение языка текста
    text_en = "This is an example text in English. It contains features of the English language."
    result = detector.detect(text_en)
    print(f"Определен язык: {result['language']}, уверенность: {result['confidence']:.2f}")
    
    # Определение языка текста с уверенностью
    text_uk = "Це приклад тексту українською мовою. Він містить особливості української мови."
    result = detector.detect(text_uk)
    print(f"Определен язык: {result['language']}, уверенность: {result['confidence']:.2f}")


def analyze_text_example():
    """Пример подробного анализа текста."""
    print("\n=== Подробный анализ текста ===")
    
    detector = LangDetector(languages=['russian', 'ukrainian', 'english', 'belarusian', 'polish'])
    
    text = """
    Это текст на русском языке для демонстрации возможностей библиотеки LangDefLib.
    Библиотека определяет язык текста с использованием различных признаков,
    таких как уникальные буквы, частотные буквы, окончания слов, маркерные слова и другие.
    """
    
    analysis = detector.analyze(text)
    
    print(f"Определен язык: {analysis['language']}")
    print(f"Уверенность: {analysis['confidence']:.2f}")
    print("\nCтатистика текста:")
    for key, value in analysis['stats'].items():
        print(f"  - {key}: {value}")
    
    print("\nТоп наиболее вероятных языков:")
    for lang in analysis['top_languages']:
        print(f"  - {lang['language']}: {lang['confidence']:.2f}")
    
    print("\nМетрики (уникальные буквы):")
    for lang, score in analysis['metrics']['unique_letters'].items():
        print(f"  - {lang}: {score}")


def multilingual_example():
    """Пример работы с несколькими языками."""
    print("\n=== Работа с несколькими языками ===")
    
    detector = LangDetector(languages=['russian', 'ukrainian', 'english', 'belarusian', 'polish'])
    
    examples = {
        'russian': "Это текст на русском языке.",
        'ukrainian': "Це текст українською мовою.",
        'english': "This is a text in English.",
        'belarusian': "Гэта тэкст на беларускай мове.",
        'polish': "To jest tekst w języku polskim.",
        'mixed_ru_en': "This is a mixed текст с английскими and русскими словами.",
        'unknown': "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    }
    
    for name, text in examples.items():
        result = detector.detect(text)
        print(f"{name}: определен как {result['language']} (уверенность: {result['confidence']:.2f})")


def custom_language_example():
    """Пример добавления собственного языка."""
    print("\n=== Добавление собственного языка ===")
    
    detector = LangDetector(languages=['russian', 'english'])
    
    # Добавляем немецкий язык
    german_data = {
        'unique_letters': ['ä', 'ö', 'ü', 'ß'],
        'frequent_letters': ['ä', 'ö', 'ü', 'ß'],
        'word_endings': ['en', 'er', 'ung', 'ich', 'lich', 'ig', 'keit', 'heit', 'schaft'],
        'marker_words': ['und', 'oder', 'aber', 'der', 'die', 'das', 'in', 'mit', 'für', 'von', 'zu'],
        'digrams': ['ch', 'ck', 'ei', 'ie', 'sch', 'st', 'th'],
        'trigrams': ['sch', 'che', 'ein', 'ich', 'und', 'den'],
        'alphabet': 'abcdefghijklmnopqrstuvwxyzäöüß'
    }
    
    detector.add_language('german', german_data)
    
    # Проверяем немецкий текст
    german_text = "Dies ist ein Beispieltext in deutscher Sprache mit Buchstaben wie ä, ö, ü und ß."
    result = detector.detect(german_text)
    print(f"Немецкий текст определен как: {result['language']} (уверенность: {result['confidence']:.2f})")
    
    # Удаляем язык
    detector.remove_language('german')
    result = detector.detect(german_text)
    print(f"После удаления немецкого языка текст определен как: {result['language']} (уверенность: {result['confidence']:.2f})")


def file_example():
    """Пример работы с файлами."""
    print("\n=== Работа с файлами ===")
    
    # Создаем временный файл с текстом
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
        f.write("""
        This is an example text in English.
        It contains multiple lines and demonstrates
        how the library can detect language from a file.
        """)
        file_path = f.name
    
    try:
        detector = LangDetector(languages=['russian', 'english', 'ukrainian'])
        result = detector.detect_from_file(file_path)
        print(f"Язык файла: {result['language']} (уверенность: {result['confidence']:.2f})")
        
        # Создание файла с данными о языке
        lang_data_dir = tempfile.mkdtemp()
        lang_file = detector.create_language_data_file('english', 
                                                      detector.BUILTIN_LANGUAGE_DATA['english'],
                                                      lang_data_dir)
        print(f"Файл с данными о языке создан: {lang_file}")
    finally:
        # Удаляем временные файлы
        os.unlink(file_path)
        if os.path.exists(lang_file):
            os.unlink(lang_file)
        os.rmdir(lang_data_dir)


def run_all_examples():
    """Запускает все примеры."""
    print("*** Примеры использования библиотеки LangDefLib ***")
    
    basic_usage()
    analyze_text_example()
    multilingual_example()
    custom_language_example()
    file_example()
    
    print("\n*** Все примеры выполнены успешно ***")


if __name__ == "__main__":
    run_all_examples() 