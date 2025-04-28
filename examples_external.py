#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Примеры использования внешних библиотек для определения языка текста.
"""

try:
    from LangDefLib import ExternalDetector, detect_language_external
except ImportError:
    print("Ошибка импорта: убедитесь, что у вас установлены необходимые библиотеки:")
    print("  pip install fasttext-wheel langdetect")
    exit(1)


def basic_usage():
    """Базовое использование внешних библиотек."""
    print("\n=== Базовое использование внешних библиотек ===")
    
    # Быстрое определение языка с использованием fastText
    text_ru = "Это пример текста на русском языке. Он содержит особенности русского языка."
    
    try:
        result = detect_language_external(text_ru, method='fasttext')
        print(f"fastText: определен язык: {result.get('language', 'unknown')}, уверенность: {result.get('confidence', 0.0):.2f}")
    except Exception as e:
        print(f"fastText: ошибка - {str(e)}")
    
    # Быстрое определение языка с использованием langdetect
    try:
        result = detect_language_external(text_ru, method='langdetect')
        print(f"langdetect: определен язык: {result.get('language', 'unknown')}, уверенность: {result.get('confidence', 0.0):.2f}")
    except Exception as e:
        print(f"langdetect: ошибка - {str(e)}")
    
    # Голосование всех методов
    try:
        result = detect_language_external(text_ru, method='vote')
        print(f"Голосование: определен язык: {result.get('language', 'unknown')}, "
              f"уверенность: {result.get('confidence', 0.0):.2f}, голосов: {result.get('votes', '?')}")
    except Exception as e:
        print(f"Голосование: ошибка - {str(e)}")
    
    # Автоматический выбор метода
    try:
        result = detect_language_external(text_ru)
        print(f"Автоматически: определен язык: {result.get('language', 'unknown')}, уверенность: {result.get('confidence', 0.0):.2f}")
    except Exception as e:
        print(f"Автоматически: ошибка - {str(e)}")


def multilingual_comparison():
    """Сравнение различных методов на разных языках."""
    print("\n=== Сравнение методов на разных языках ===")
    
    examples = {
        'ru': "Это пример текста на русском языке.",
        'uk': "Це приклад тексту українською мовою.",
        'en': "This is an example text in English.",
        'fr': "C'est un exemple de texte en français.",
        'de': "Dies ist ein Beispieltext in deutscher Sprache.",
        'es': "Este es un texto de ejemplo en español.",
        'it': "Questo è un testo di esempio in italiano.",
        'pt': "Este é um texto de exemplo em português.",
        'nl': "Dit is een voorbeeldtekst in het Nederlands.",
        'pl': "To jest przykładowy tekst w języku polskim.",
        'ar': "هذا مثال على النص باللغة العربية.",
        'zh': "这是一个中文示例文本。",
        'ja': "これは日本語のサンプルテキストです。",
        'ko': "이것은 한국어 예제 텍스트입니다."
    }
    
    detector = ExternalDetector()
    
    # Проходим по всем примерам
    for lang, text in examples.items():
        print(f"\nЯзык: {lang}, текст: {text}")
        
        try:
            # Получаем результаты всех методов
            results = detector.detect_with_all_methods(text)
            
            # Выводим результаты каждого метода
            if results.get('fasttext'):
                print(f"  fastText: {results['fasttext'].get('language', 'unknown')} "
                      f"(уверенность: {results['fasttext'].get('confidence', 0.0):.2f})")
            
            if results.get('langdetect'):
                print(f"  langdetect: {results['langdetect'].get('language', 'unknown')} "
                      f"(уверенность: {results['langdetect'].get('confidence', 0.0):.2f})")
            
            if results.get('vote'):
                votes_info = f", голосов: {results['vote'].get('votes', '?')}/{results['vote'].get('total_votes', '?')}" \
                    if 'votes' in results['vote'] else ""
                print(f"  Голосование: {results['vote'].get('language', 'unknown')} "
                      f"(уверенность: {results['vote'].get('confidence', 0.0):.2f}{votes_info})")
            
            # Выводим лучший метод
            if results.get('best_method') and results.get('best'):
                print(f"  Лучший метод: {results['best_method']} -> {results['best'].get('language', 'unknown')} "
                      f"(уверенность: {results['best'].get('confidence', 0.0):.2f})")
        except Exception as e:
            print(f"  Ошибка при определении языка: {str(e)}")


def short_text_examples():
    """Примеры определения языка коротких текстов."""
    print("\n=== Определение языка коротких текстов ===")
    
    short_texts = [
        "Hi",
        "Hello",
        "Привет",
        "Bonjour",
        "Hola",
        "Ciao",
        "こんにちは",
        "안녕하세요",
        "你好"
    ]
    
    detector = ExternalDetector()
    
    for text in short_texts:
        print(f"\nТекст: {text}")
        
        # Получаем результаты всех методов
        results = detector.detect_with_all_methods(text)
        
        # Выводим лучший метод
        print(f"  Лучший метод: {results['best_method']} -> {results['best']['language']} "
              f"(уверенность: {results['best']['confidence']:.2f})")


def fasttext_model_comparison():
    """Сравнение маленькой и большой моделей fastText."""
    print("\n=== Сравнение моделей fastText ===")
    
    # Проверяем, доступны ли обе модели fastText
    import os
    
    small_model_path = 'lid.176.ftz'
    big_model_path = 'lid.176.bin'
    
    if not os.path.exists(small_model_path):
        print(f"Маленькая модель fastText не найдена по пути: {small_model_path}")
        print("Скачайте её: wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz")
    
    if not os.path.exists(big_model_path):
        print(f"Большая модель fastText не найдена по пути: {big_model_path}")
        print("Скачайте её: wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin")
    
    if not os.path.exists(small_model_path) or not os.path.exists(big_model_path):
        print("Невозможно выполнить сравнение моделей. Скачайте модели и повторите попытку.")
        return
    
    # Создаем детекторы с разными моделями
    detector_small = ExternalDetector(
        use_langdetect=False, 
        fasttext_model_path=small_model_path,
        fasttext_model_size='small'
    )
    
    detector_big = ExternalDetector(
        use_langdetect=False, 
        fasttext_model_path=big_model_path,
        fasttext_model_size='big'
    )
    
    examples = {
        'short_en': "Hi there",
        'short_ru': "Привет",
        'medium_en': "This is a medium length text in English.",
        'medium_ru': "Это текст средней длины на русском языке.",
        'long_en': "This is a longer text in English that should provide more context for language detection. It includes multiple sentences and should be easier to detect correctly.",
        'long_ru': "Это более длинный текст на русском языке, который должен предоставить больше контекста для определения языка. Он включает несколько предложений и должен быть легче определен правильно."
    }
    
    for name, text in examples.items():
        print(f"\nТекст ({name}): {text}")
        
        # Определяем язык с маленькой моделью
        result_small = detector_small.detect(text, method='fasttext')
        print(f"  Маленькая модель: {result_small['language']} (уверенность: {result_small['confidence']:.2f})")
        
        # Определяем язык с большой моделью
        result_big = detector_big.detect(text, method='fasttext')
        print(f"  Большая модель: {result_big['language']} (уверенность: {result_big['confidence']:.2f})")


def run_all_examples():
    """Запускает все примеры."""
    print("*** Примеры использования внешних библиотек для определения языка ***")
    
    basic_usage()
    multilingual_comparison()
    short_text_examples()
    # fasttext_model_comparison()  # Раскомментируйте, если у вас есть обе модели fastText
    
    print("\n*** Все примеры выполнены успешно ***")


if __name__ == "__main__":
    run_all_examples() 
