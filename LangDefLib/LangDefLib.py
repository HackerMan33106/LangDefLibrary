#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LangDefLib - библиотека для определения языка текста без внешних зависимостей

Пример использования:
    from LangDefLib import LangDetector
    
    detector = LangDetector()
    result = detector.detect("Это пример текста на русском языке")
    print(result)  # {'language': 'russian', 'confidence': 0.95}
    
    # Использование с другими языками
    detector = LangDetector(languages=['russian', 'ukrainian', 'belarusian', 'english'])
    result = detector.detect("This is an example text in English")
    print(result)  # {'language': 'english', 'confidence': 0.99}
    
    # Получение подробного анализа
    analysis = detector.analyze("Це приклад тексту українською мовою")
    print(analysis)
"""

import re
import os
import json
from typing import List, Dict, Union, Tuple, Set, Optional, Any


class LanguageData:
    """
    Класс для хранения данных о языке для определения текста.
    """
    
    def __init__(self, name: str, data: Dict[str, Any]):
        """
        Инициализирует данные для определенного языка.
        
        Args:
            name (str): Код языка (например, 'russian', 'ukrainian')
            data (Dict[str, Any]): Словарь с данными о языке
        """
        self.name = name
        self.unique_letters = set(data.get('unique_letters', []))
        self.frequent_letters = set(data.get('frequent_letters', []))
        self.word_endings = data.get('word_endings', [])
        self.marker_words = set(data.get('marker_words', []))
        self.digrams = data.get('digrams', [])
        self.trigrams = data.get('trigrams', [])
        self.alphabet = set(data.get('alphabet', []))
        self.weights = data.get('weights', {
            'unique_letters': 2.0,
            'frequent_letters': 1.0,
            'word_endings': 1.5,
            'marker_words': 3.0,
            'digrams': 1.0,
            'trigrams': 1.2
        })


class LangDetector:
    """
    Класс для определения языка текста без использования внешних зависимостей.
    
    Поддерживаемые языки по умолчанию: русский и украинский.
    Может быть расширен дополнительными языками.
    """
    
    # Пути к данным языков
    DEFAULT_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    
    # Поддерживаемые языки по умолчанию
    DEFAULT_LANGUAGES = ['russian', 'ukrainian']
    
    # Встроенные данные о языках (используются, если файлы не найдены)
    BUILTIN_LANGUAGE_DATA = {
        'russian': {
            'unique_letters': ['ы', 'ъ', 'э'],
            'frequent_letters': ['ы', 'ъ', 'э', 'ё'],
            'word_endings': [
                'ого', 'его', 'ому', 'ему', 'ой', 'ый', 'ий', 'ться',
                'тся', 'ешь', 'ет', 'ем', 'ете', 'ут', 'ют', 'ят',
                'ать', 'ить', 'оть', 'уть', 'еть', 'ых', 'их'
            ],
            'marker_words': [
                'это', 'или', 'как', 'который', 'где', 'когда',
                'словно', 'потому', 'кто', 'также', 'от', 'из', 'до',
                'в', 'при', 'для', 'и', 'но', 'однако',
                'хотя', 'чтобы', 'если', 'из-за', 'поэтому', 'ещё', 'да', 
                'нет', 'был', 'была', 'было', 'были'
            ],
            'digrams': [
                'ть', 'тс', 'ск', 'ый', 'ий', 'тьс', 'ться', 'тс', 'нн', 'жи', 'ши',
                'чн', 'чк', 'ни', 'не', 'на', 'по', 'вы', 'за', 'что', 'ли', 'ой', 'ом'
            ],
            'trigrams': ['тся', 'ться', 'ани', 'ени', 'ост', 'ств', 'ние'],
            'alphabet': 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        },
        'ukrainian': {
            'unique_letters': ['є', 'і', 'ї', 'ґ'],
            'frequent_letters': ['і', 'є', 'ї', 'ґ', 'ь'],
            'word_endings': [
                'ою', 'ою', 'ого', 'ої', 'ий', 'ій', 'ися', 'ись',
                'ться', 'ться', 'еться', 'иться', 'ються', 'уються',
                'іти', 'ати', 'ити', 'ути', 'яти', 'емо', 'єте', 'ємо'
            ],
            'marker_words': [
                'це', 'або', 'чи', 'що', 'як', 'який', 'котрий', 'де', 'коли',
                'наче', 'бо', 'тому', 'хто', 'також', 'від', 'з', 'із', 'зі',
                'до', 'у', 'при', 'для', 'та', 'і', 'й', 'але', 'проте', 'однак',
                'хоча', 'щоб', 'якщо', 'коли', 'через', 'тому', 'ще', 'так', 
                'ні', 'не', 'є', 'був', 'була', 'було', 'були'
            ],
            'digrams': [
                'ть', 'нн', 'ськ', 'ий', 'ій', 'тьс', 'ьс', 'ьк', 'нн', 'дз', 'дж',
                'ґу', 'ці', 'не', 'на', 'по', 'ви', 'за', 'що', 'чи', 'ої', 'ою'
            ],
            'trigrams': ['ння', 'ськ', 'ість', 'ува', 'іст', 'ють'],
            'alphabet': 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
        },
        'belarusian': {
            'unique_letters': ['ў', 'і', 'ь'],
            'frequent_letters': ['ў', 'і', 'ь'],
            'word_endings': [
                'аць', 'яць', 'ець', 'іць', 'ыць', 'ога', 'ага', 'яго', 'ай',
                'ую', 'юю', 'ам', 'ям', 'аў', 'яў', 'ы', 'і', 'а', 'я'
            ],
            'marker_words': [
                'гэта', 'ці', 'як', 'які', 'дзе', 'калі', 'хто', 'таксама',
                'ад', 'з', 'да', 'у', 'пры', 'для', 'і', 'але', 'аднак',
                'хоць', 'каб', 'калі', 'яшчэ', 'так', 'не', 'быў', 'была', 'было', 'былі'
            ],
            'digrams': [
                'дз', 'ць', 'нн', 'ў', 'ы', 'і', 'ь', 'ск', 'аў', 'яў'
            ],
            'trigrams': ['дзь', 'цца', 'чны', 'нне', 'ван', 'льн'],
            'alphabet': 'абвгдеёжзійклмнопрстуўфхцчшыьэюя'
        },
        'english': {
            'unique_letters': [],
            'frequent_letters': ['w', 'q', 'x', 'y', 'k'],
            'word_endings': [
                'ing', 'ed', 'ly', 'tion', 'sion', 'ment', 'ness', 'ity',
                'ance', 'ence', 'er', 'or', 'ist', 's', 'es'
            ],
            'marker_words': [
                'the', 'and', 'is', 'are', 'was', 'were', 'be', 'been',
                'to', 'of', 'in', 'for', 'with', 'on', 'at', 'from',
                'by', 'about', 'as', 'into', 'like', 'through', 'after',
                'over', 'between', 'out', 'but', 'or', 'so', 'if', 'while'
            ],
            'digrams': [
                'th', 'he', 'an', 'in', 'er', 'on', 'at', 're', 'ed', 'nd',
                'to', 'or', 'ea', 'ti', 'ar', 'te', 'al', 'st', 'en', 'it'
            ],
            'trigrams': ['the', 'and', 'ing', 'ion', 'ent', 'ati', 'for', 'her', 'ter', 'hat'],
            'alphabet': 'abcdefghijklmnopqrstuvwxyz'
        },
        'polish': {
            'unique_letters': ['ą', 'ę', 'ł', 'ń', 'ó', 'ś', 'ź', 'ż'],
            'frequent_letters': ['ą', 'ę', 'ł', 'ń', 'ó', 'ś', 'ź', 'ż', 'cz', 'sz', 'rz'],
            'word_endings': [
                'ać', 'ąć', 'eć', 'yć', 'ść', 'ości', 'owa', 'nego', 'emu',
                'ymi', 'ych', 'ego', 'em', 'cie', 'ują', 'ają'
            ],
            'marker_words': [
                'to', 'jest', 'nie', 'tak', 'jak', 'który', 'gdzie', 'kiedy',
                'od', 'z', 'ze', 'do', 'w', 'przy', 'dla', 'i', 'ale', 'jednak',
                'chociaż', 'żeby', 'jeśli', 'przez', 'więc', 'jeszcze'
            ],
            'digrams': [
                'cz', 'sz', 'rz', 'dz', 'ch', 'ni', 'ci', 'ąc', 'ść', 'że'
            ],
            'trigrams': ['nie', 'prz', 'owa', 'ści', 'czn', 'dzi', 'anie'],
            'alphabet': 'aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż'
        }
    }
    
    def __init__(self, languages: List[str] = None, data_dir: str = None, min_confidence: float = 0.6):
        """
        Инициализирует детектор языка.
        
        Args:
            languages (List[str], optional): Список языков для детекции. 
                                           По умолчанию ['russian', 'ukrainian'].
            data_dir (str, optional): Путь к директории с данными о языках.
                                     По умолчанию директория 'data' рядом с файлом библиотеки.
            min_confidence (float, optional): Минимальный порог уверенности для определения языка.
                                            По умолчанию 0.6 (60%).
        """
        self.languages = languages or self.DEFAULT_LANGUAGES
        self.data_dir = data_dir or self.DEFAULT_DATA_DIR
        self.min_confidence = min_confidence
        
        # Загружаем данные о языках
        self.language_data = {}
        self._load_language_data()
    
    def _load_language_data(self) -> None:
        """
        Загружает данные о языках из файлов или встроенных данных.
        """
        for lang in self.languages:
            lang_file = os.path.join(self.data_dir, f"{lang}.json")
            
            # Пытаемся загрузить данные из файла
            try:
                if os.path.exists(lang_file):
                    with open(lang_file, 'r', encoding='utf-8') as f:
                        lang_data = json.load(f)
                        self.language_data[lang] = LanguageData(lang, lang_data)
                else:
                    # Если файл не найден, используем встроенные данные
                    if lang in self.BUILTIN_LANGUAGE_DATA:
                        self.language_data[lang] = LanguageData(lang, self.BUILTIN_LANGUAGE_DATA[lang])
                    else:
                        print(f"Предупреждение: данные для языка '{lang}' не найдены.")
            except Exception as e:
                print(f"Ошибка при загрузке данных для языка '{lang}': {e}")
                # Если произошла ошибка, используем встроенные данные как запасной вариант
                if lang in self.BUILTIN_LANGUAGE_DATA:
                    self.language_data[lang] = LanguageData(lang, self.BUILTIN_LANGUAGE_DATA[lang])
    
    def add_language(self, lang_code: str, data: Dict[str, Any]) -> None:
        """
        Добавляет новый язык для детекции.
        
        Args:
            lang_code (str): Код языка (например, 'german')
            data (Dict[str, Any]): Словарь с данными о языке
        """
        if lang_code not in self.languages:
            self.languages.append(lang_code)
        
        self.language_data[lang_code] = LanguageData(lang_code, data)
    
    def remove_language(self, lang_code: str) -> bool:
        """
        Удаляет язык из списка детекции.
        
        Args:
            lang_code (str): Код языка для удаления
            
        Returns:
            bool: True если язык был удален, False если язык не был найден
        """
        if lang_code in self.languages:
            self.languages.remove(lang_code)
            if lang_code in self.language_data:
                del self.language_data[lang_code]
            return True
        return False
    
    def _clean_text(self, text: str) -> str:
        """
        Очищает текст от знаков препинания и приводит к нижнему регистру.
        
        Args:
            text (str): Исходный текст
            
        Returns:
            str: Очищенный текст
        """
        # Приводим к нижнему регистру
        text = text.lower()
        
        # Заменяем все знаки препинания на пробелы
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Заменяем множественные пробелы на один
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def _count_unique_letters(self, text: str) -> Dict[str, int]:
        """
        Подсчитывает количество уникальных букв для каждого языка в тексте.
        
        Args:
            text (str): Текст для анализа
            
        Returns:
            Dict[str, int]: Словарь {'language_code': score}
        """
        scores = {}
        
        for lang_code, lang_data in self.language_data.items():
            scores[lang_code] = sum(1 for char in text if char in lang_data.unique_letters)
        
        return scores
    
    def _count_frequent_letters(self, text: str) -> Dict[str, int]:
        """
        Подсчитывает количество частотных букв для каждого языка в тексте.
        
        Args:
            text (str): Текст для анализа
            
        Returns:
            Dict[str, int]: Словарь {'language_code': score}
        """
        scores = {}
        
        for lang_code, lang_data in self.language_data.items():
            scores[lang_code] = sum(1 for char in text if char in lang_data.frequent_letters)
        
        return scores
    
    def _check_word_endings(self, words: List[str]) -> Dict[str, int]:
        """
        Анализирует окончания слов для определения языка.
        
        Args:
            words (List[str]): Список слов для анализа
            
        Returns:
            Dict[str, int]: Словарь {'language_code': score}
        """
        scores = {lang: 0 for lang in self.languages}
        
        for word in words:
            if len(word) < 3:
                continue
            
            for lang_code, lang_data in self.language_data.items():
                for ending in lang_data.word_endings:
                    if word.endswith(ending):
                        scores[lang_code] += 1
                        break
        
        return scores
    
    def _check_marker_words(self, words: List[str]) -> Dict[str, int]:
        """
        Проверяет наличие маркерных слов в тексте.
        
        Args:
            words (List[str]): Список слов для анализа
            
        Returns:
            Dict[str, int]: Словарь {'language_code': score}
        """
        scores = {lang: 0 for lang in self.languages}
        
        # Приводим слова к нижнему регистру для сравнения
        words_lower = [word.lower() for word in words]
        
        for word in words_lower:
            for lang_code, lang_data in self.language_data.items():
                if word in lang_data.marker_words:
                    scores[lang_code] += 1
        
        return scores
    
    def _check_ngrams(self, text: str, n: int = 2) -> Dict[str, int]:
        """
        Проверяет наличие характерных n-грамм в тексте.
        
        Args:
            text (str): Текст для анализа
            n (int): Размер n-граммы (2 для диграмм, 3 для триграмм)
            
        Returns:
            Dict[str, int]: Словарь {'language_code': score}
        """
        scores = {lang: 0 for lang in self.languages}
        
        text_lower = text.lower()
        
        for lang_code, lang_data in self.language_data.items():
            if n == 2 and hasattr(lang_data, 'digrams'):
                for digram in lang_data.digrams:
                    scores[lang_code] += text_lower.count(digram)
            elif n == 3 and hasattr(lang_data, 'trigrams'):
                for trigram in lang_data.trigrams:
                    scores[lang_code] += text_lower.count(trigram)
        
        return scores
    
    def _calculate_weighted_scores(self, 
                                  unique_letters: Dict[str, int],
                                  frequent_letters: Dict[str, int],
                                  word_endings: Dict[str, int],
                                  marker_words: Dict[str, int],
                                  digrams: Dict[str, int],
                                  trigrams: Dict[str, int]) -> Dict[str, float]:
        """
        Рассчитывает взвешенные баллы для каждого языка.
        
        Args:
            unique_letters (Dict[str, int]): Баллы по уникальным буквам
            frequent_letters (Dict[str, int]): Баллы по частотным буквам
            word_endings (Dict[str, int]): Баллы по окончаниям слов
            marker_words (Dict[str, int]): Баллы по маркерным словам
            digrams (Dict[str, int]): Баллы по диграммам
            trigrams (Dict[str, int]): Баллы по триграммам
            
        Returns:
            Dict[str, float]: Словарь с общими взвешенными баллами для каждого языка
        """
        scores = {lang: 0.0 for lang in self.languages}
        
        for lang_code, lang_data in self.language_data.items():
            scores[lang_code] = (
                unique_letters.get(lang_code, 0) * lang_data.weights.get('unique_letters', 2.0) +
                frequent_letters.get(lang_code, 0) * lang_data.weights.get('frequent_letters', 1.0) +
                word_endings.get(lang_code, 0) * lang_data.weights.get('word_endings', 1.5) +
                marker_words.get(lang_code, 0) * lang_data.weights.get('marker_words', 3.0) +
                digrams.get(lang_code, 0) * lang_data.weights.get('digrams', 1.0) +
                trigrams.get(lang_code, 0) * lang_data.weights.get('trigrams', 1.2)
            )
        
        return scores
    
    def detect(self, text: str) -> Dict[str, Any]:
        """
        Определяет язык текста и возвращает результат с уверенностью.
        
        Args:
            text (str): Текст для анализа
            
        Returns:
            Dict[str, Any]: Словарь с результатом {'language': str, 'confidence': float}
        """
        if not text or not isinstance(text, str):
            return {'language': 'unknown', 'confidence': 0.0}
        
        # Очищаем текст
        cleaned_text = self._clean_text(text)
        
        # Если текст пустой после очистки
        if not cleaned_text:
            return {'language': 'unknown', 'confidence': 0.0}
        
        # Разбиваем на слова
        words = cleaned_text.split()
        
        # Если нет слов
        if not words:
            return {'language': 'unknown', 'confidence': 0.0}
        
        # Быстрая проверка на уникальные буквы
        unique_scores = self._count_unique_letters(cleaned_text)
        
        # Если есть явные признаки одного языка по уникальным буквам
        for lang, score in unique_scores.items():
            if score > 0 and all(s == 0 for l, s in unique_scores.items() if l != lang):
                return {'language': lang, 'confidence': 0.95}
        
        # Полный анализ
        frequent_letters = self._count_frequent_letters(cleaned_text)
        word_endings = self._check_word_endings(words)
        marker_words = self._check_marker_words(words)
        digrams = self._check_ngrams(cleaned_text, n=2)
        trigrams = self._check_ngrams(cleaned_text, n=3)
        
        # Рассчитываем взвешенные баллы
        scores = self._calculate_weighted_scores(
            unique_scores,
            frequent_letters,
            word_endings,
            marker_words,
            digrams,
            trigrams
        )
        
        # Общая сумма баллов
        total_score = sum(scores.values())
        
        # Определяем язык и уверенность
        if total_score == 0:
            return {'language': 'unknown', 'confidence': 0.0}
        
        # Находим язык с наивысшим баллом
        best_lang = max(scores.items(), key=lambda x: x[1])
        language = best_lang[0]
        confidence = best_lang[1] / total_score
        
        # Если уверенность ниже порога, возвращаем "unknown"
        if confidence < self.min_confidence:
            return {'language': 'unknown', 'confidence': confidence}
        
        return {
            'language': language,
            'confidence': confidence
        }
    
    def detect_from_file(self, file_path: str) -> Dict[str, Any]:
        """
        Определяет язык текста из файла.
        
        Args:
            file_path (str): Путь к файлу с текстом
            
        Returns:
            Dict[str, Any]: Словарь с результатом {'language': str, 'confidence': float}
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return self.detect(text)
        except Exception as e:
            return {'language': 'unknown', 'confidence': 0.0, 'error': str(e)}
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Проводит подробный анализ текста и возвращает все метрики.
        
        Args:
            text (str): Текст для анализа
            
        Returns:
            Dict[str, Any]: Подробная информация о результатах анализа
        """
        if not text or not isinstance(text, str):
            return {'error': 'Empty or invalid text'}
        
        # Очищаем текст
        cleaned_text = self._clean_text(text)
        
        # Если текст пустой после очистки
        if not cleaned_text:
            return {'error': 'Text contains no analyzable content'}
        
        # Разбиваем на слова
        words = cleaned_text.split()
        
        # Собираем все метрики
        unique_letters = self._count_unique_letters(cleaned_text)
        frequent_letters = self._count_frequent_letters(cleaned_text)
        word_endings = self._check_word_endings(words)
        marker_words = self._check_marker_words(words)
        digrams = self._check_ngrams(cleaned_text, n=2)
        trigrams = self._check_ngrams(cleaned_text, n=3)
        
        # Рассчитываем взвешенные баллы
        scores = self._calculate_weighted_scores(
            unique_letters,
            frequent_letters,
            word_endings,
            marker_words,
            digrams,
            trigrams
        )
        
        # Общая сумма баллов
        total_score = sum(scores.values())
        
        # Определяем язык и уверенность
        if total_score == 0:
            result = {'language': 'unknown', 'confidence': 0.0}
        else:
            # Находим язык с наивысшим баллом
            best_lang = max(scores.items(), key=lambda x: x[1])
            language = best_lang[0]
            confidence = best_lang[1] / total_score
            
            # Если уверенность ниже порога, возвращаем "unknown"
            if confidence < self.min_confidence:
                result = {'language': 'unknown', 'confidence': confidence}
            else:
                result = {'language': language, 'confidence': confidence}
        
        # Добавляем базовую статистику
        result['stats'] = {
            'text_length': len(text),
            'cleaned_length': len(cleaned_text),
            'word_count': len(words),
            'average_word_length': sum(len(word) for word in words) / len(words) if words else 0
        }
        
        # Добавляем метрики
        result['metrics'] = {
            'unique_letters': unique_letters,
            'frequent_letters': frequent_letters,
            'word_endings': word_endings,
            'marker_words': marker_words,
            'digrams': digrams,
            'trigrams': trigrams
        }
        
        # Добавляем баллы
        result['scores'] = scores
        
        # Определяем наиболее вероятные языки (топ-3)
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        result['top_languages'] = [
            {'language': lang, 'score': score, 'confidence': score / total_score if total_score > 0 else 0}
            for lang, score in sorted_scores[:3] if score > 0
        ]
        
        return result
    
    def create_language_data_file(self, lang_code: str, data: Dict[str, Any], output_dir: str = None) -> str:
        """
        Создает JSON-файл с данными о языке.
        
        Args:
            lang_code (str): Код языка (например, 'german')
            data (Dict[str, Any]): Словарь с данными о языке
            output_dir (str, optional): Директория для сохранения файла.
                                      По умолчанию используется self.data_dir.
                                      
        Returns:
            str: Путь к созданному файлу
        """
        output_dir = output_dir or self.data_dir
        
        # Создаем директорию, если она не существует
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        file_path = os.path.join(output_dir, f"{lang_code}.json")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        return file_path

    def get_language(self, text: str) -> str:
        """
        Определяет язык текста и возвращает только код языка (без дополнительной информации).
        
        Args:
            text (str): Текст для анализа
            
        Returns:
            str: Код языка ('russian', 'ukrainian', 'english', ...) или 'unknown'
        """
        result = self.detect(text)
        return result['language']


def detect_language(text: str, languages: List[str] = None) -> Dict[str, Any]:
    """
    Вспомогательная функция для быстрого определения языка текста.
    
    Args:
        text (str): Текст для анализа
        languages (List[str], optional): Список языков для детекции.
                                        По умолчанию используются все доступные языки.
                                        
    Returns:
        Dict[str, Any]: Словарь с результатом {'language': str, 'confidence': float}
    """
    detector = LangDetector(languages=languages)
    return detector.detect(text)


# Пример использования
def main():
    detector = LangDetector()
    
    # Примеры текстов
    examples = {
        'russian': "Это текст на русском языке с использованием ы, ъ и других букв. В русском языке есть особенности, которые отличают его от украинского.",
        'ukrainian': "Це текст українською мовою з використанням ї, і, є та інших літер. В українській мові є особливості, які відрізняють її від російської.",
        'belarusian': "Гэта тэкст на беларускай мове з выкарыстаннем спецыфічных літар ў і і. У беларускай мове ёсць асаблівасці, якія адрозніваюць яе ад рускай і ўкраінскай.",
        'english': "This is a text in English. It has certain features that distinguish it from Slavic languages.",
        'polish': "To jest tekst w języku polskim z użyciem ą, ę, ł, ń, ó, ś, ź, ż i innych liter. W języku polskim są cechy, które odróżniają go od innych języków słowiańskich.",
        'ambiguous': "Мама мыла раму. Она пошла домой."
    }
    
    print("Базовое определение языка:")
    for lang, text in examples.items():
        result = detector.detect(text)
        print(f"{lang}: определен как {result['language']} (уверенность: {result['confidence']:.2f})")
    
    print("\nОпределение с использованием всех языков:")
    all_detector = LangDetector(languages=['russian', 'ukrainian', 'belarusian', 'english', 'polish'])
    for lang, text in examples.items():
        result = all_detector.detect(text)
        print(f"{lang}: определен как {result['language']} (уверенность: {result['confidence']:.2f})")
    
    print("\nПодробный анализ текста на русском языке:")
    analysis = all_detector.analyze(examples['russian'])
    print(f"Язык: {analysis['language']}")
    print(f"Уверенность: {analysis['confidence']:.2f}")
    print(f"Топ языков: {analysis['top_languages']}")
    print(f"Статистика: {analysis['stats']}")
    
    # Использование вспомогательной функции
    print("\nИспользование вспомогательной функции:")
    result = detect_language("This is a simple English text", languages=['english', 'russian'])
    print(f"Определен язык: {result['language']} (уверенность: {result['confidence']:.2f})")
    
if __name__ == "__main__":
    main() 