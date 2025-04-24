#!/usr/bin/env python
# -*- coding: utf-8 -*-

class LangDetector:
    """
    Класс для определения языка текста (русский или украинский)
    без использования внешних зависимостей.
    """
    
    def __init__(self):
        # Уникальные буквы для русского языка
        self.russian_unique = set(['ы', 'ъ', 'э'])
        
        # Уникальные буквы для украинского языка
        self.ukrainian_unique = set(['є', 'і', 'ї', 'ґ'])
        
        # Буквы, которые чаще встречаются в украинском
        self.uk_frequent = set(['і', 'є', 'ї', 'ґ', 'ь'])
        
        # Буквы, которые чаще встречаются в русском
        self.ru_frequent = set(['ы', 'ъ', 'э'])
        
        # Типичные украинские окончания слов
        self.ukrainian_endings = [
            'ою', 'ою', 'ого', 'ої', 'ий', 'ій', 'ися', 'ись',
            'ться', 'ться', 'еться', 'иться', 'ються', 'уються',
            'іти', 'ати', 'ити', 'ути', 'яти', 'емо', 'єте', 'ємо'
        ]
        
        # Типичные русские окончания слов
        self.russian_endings = [
            'ого', 'его', 'ому', 'ему', 'ой', 'ый', 'ий', 'ться',
            'тся', 'ешь', 'ет', 'ем', 'ете', 'ут', 'ют', 'ят',
            'ать', 'ить', 'оть', 'уть', 'еть', 'ых', 'их'
        ]
        
        # Маркерные слова для украинского языка
        self.ukrainian_words = [
            'це', 'або', 'чи', 'що', 'як', 'який', 'котрий', 'де', 'коли',
            'наче', 'бо', 'тому', 'хто', 'також', 'від', 'з', 'із', 'зі',
            'до', 'у', 'при', 'для', 'та', 'і', 'й', 'але', 'проте', 'однак',
            'хоча', 'щоб', 'якщо', 'коли', 'через', 'тому', 'ще', 'так', 
            'ні', 'не', 'є', 'був', 'була', 'було', 'були'
        ]
        
        # Маркерные слова для русского языка
        self.russian_words = [
            'это', 'или', 'как', 'который', 'где', 'когда',
            'словно', 'потому', 'кто', 'также', 'от', 'из', 'до',
            'в', 'при', 'для', 'и', 'но', 'однако',
            'хотя', 'чтобы', 'если', 'из-за', 'поэтому', 'ещё', 'да', 
            'нет', 'был', 'была', 'было', 'были'
        ]
        
        # Украинские буквосочетания (диграммы)
        self.ukrainian_digrams = [
            'ть', 'нн', 'ськ', 'ий', 'ій', 'тьс', 'ьс', 'ьк', 'нн', 'дз', 'дж',
            'ґу', 'ці', 'не', 'на', 'по', 'ви', 'за', 'що', 'чи', 'ої', 'ою'
        ]
        
        # Русские буквосочетания (диграммы)
        self.russian_digrams = [
            'ть', 'тс', 'ск', 'ый', 'ий', 'тьс', 'ться', 'тс', 'нн', 'жи', 'ши',
            'чн', 'чк', 'ни', 'не', 'на', 'по', 'вы', 'за', 'что', 'ли', 'ой', 'ом'
        ]
        
    def _count_unique_letters(self, text):
        """
        Подсчитывает количество уникальных букв для каждого языка в тексте.
        
        Args:
            text (str): Текст для анализа
            
        Returns:
            tuple: (ru_count, uk_count)
        """
        ru_unique_count = sum(1 for char in text if char in self.russian_unique)
        uk_unique_count = sum(1 for char in text if char in self.ukrainian_unique)
        
        return ru_unique_count, uk_unique_count
        
    def _count_frequent_letters(self, text):
        """
        Подсчитывает количество частотных букв для каждого языка в тексте.
        
        Args:
            text (str): Текст для анализа
            
        Returns:
            tuple: (ru_count, uk_count)
        """
        ru_char_frequency = sum(1 for char in text if char in self.ru_frequent)
        uk_char_frequency = sum(1 for char in text if char in self.uk_frequent)
        
        return ru_char_frequency, uk_char_frequency
        
    def _check_word_endings(self, words):
        """
        Анализирует окончания слов для определения языка.
        
        Args:
            words (list): Список слов для анализа
            
        Returns:
            tuple: (ru_score, uk_score)
        """
        ru_score = 0
        uk_score = 0
        
        for word in words:
            if len(word) < 3:
                continue
                
            # Проверяем украинские окончания
            for ending in self.ukrainian_endings:
                if word.endswith(ending):
                    uk_score += 1
                    break
                    
            # Проверяем русские окончания
            for ending in self.russian_endings:
                if word.endswith(ending):
                    ru_score += 1
                    break
        
        return ru_score, uk_score
        
    def _check_marker_words(self, words):
        """
        Проверяет наличие маркерных слов в тексте.
        
        Args:
            words (list): Список слов для анализа
            
        Returns:
            tuple: (ru_score, uk_score)
        """
        ru_score = 0
        uk_score = 0
        
        # Приводим слова к нижнему регистру для сравнения
        words_lower = [word.lower() for word in words]
        
        for word in words_lower:
            if word in self.ukrainian_words:
                uk_score += 1
                
            if word in self.russian_words:
                ru_score += 1
        
        return ru_score, uk_score
        
    def _check_digrams(self, text):
        """
        Проверяет наличие характерных буквосочетаний в тексте.
        
        Args:
            text (str): Текст для анализа
            
        Returns:
            tuple: (ru_score, uk_score)
        """
        ru_score = 0
        uk_score = 0
        
        text_lower = text.lower()
        
        for digram in self.ukrainian_digrams:
            uk_score += text_lower.count(digram)
            
        for digram in self.russian_digrams:
            ru_score += text_lower.count(digram)
            
        return ru_score, uk_score
        
    def _clean_text(self, text):
        """
        Очищает текст от знаков препинания и приводит к нижнему регистру.
        
        Args:
            text (str): Исходный текст
            
        Returns:
            str: Очищенный текст
        """
        import re
        
        # Приводим к нижнему регистру
        text = text.lower()
        
        # Заменяем все знаки препинания на пробелы
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Заменяем множественные пробелы на один
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
        
    def detect_language(self, text):
        """
        Определяет язык текста с использованием всех доступных методов.
        
        Args:
            text (str): Текст для анализа
            
        Returns:
            str: 'russian', 'ukrainian' или 'unknown'
        """
        if not text or not isinstance(text, str):
            return 'unknown'
            
        # Очищаем текст
        cleaned_text = self._clean_text(text)
        
        # Если текст пустой после очистки
        if not cleaned_text:
            return 'unknown'
            
        # Разбиваем на слова
        words = cleaned_text.split()
        
        # Если нет слов
        if not words:
            return 'unknown'
            
        # Проверяем уникальные буквы
        ru_unique, uk_unique = self._count_unique_letters(cleaned_text)
        
        # Если есть явные признаки одного из языков по уникальным буквам
        if ru_unique > 0 and uk_unique == 0:
            return 'russian'
        elif uk_unique > 0 and ru_unique == 0:
            return 'ukrainian'
            
        # Если нет явных признаков, проводим комплексный анализ
        scores = {
            'russian': 0,
            'ukrainian': 0
        }
        
        # Добавляем баллы на основе уникальных букв
        scores['russian'] += ru_unique * 2  # Умножаем на вес
        scores['ukrainian'] += uk_unique * 2  # Умножаем на вес
        
        # Проверяем частотные буквы
        ru_freq, uk_freq = self._count_frequent_letters(cleaned_text)
        scores['russian'] += ru_freq
        scores['ukrainian'] += uk_freq
        
        # Проверяем окончания слов
        ru_endings, uk_endings = self._check_word_endings(words)
        scores['russian'] += ru_endings * 1.5  # Умножаем на вес
        scores['ukrainian'] += uk_endings * 1.5  # Умножаем на вес
        
        # Проверяем маркерные слова
        ru_markers, uk_markers = self._check_marker_words(words)
        scores['russian'] += ru_markers * 3  # Умножаем на вес
        scores['ukrainian'] += uk_markers * 3  # Умножаем на вес
        
        # Проверяем диграммы
        ru_digrams, uk_digrams = self._check_digrams(cleaned_text)
        scores['russian'] += ru_digrams
        scores['ukrainian'] += uk_digrams
        
        # Определяем язык на основе общего количества баллов
        if scores['russian'] > scores['ukrainian']:
            return 'russian'
        elif scores['ukrainian'] > scores['russian']:
            return 'ukrainian'
        else:
            return 'unknown'
    
    def get_confidence(self, text):
        """
        Возвращает уверенность (от 0 до 1) в определении языка.
        
        Args:
            text (str): Текст для анализа
            
        Returns:
            dict: {'language': 'russian'|'ukrainian'|'unknown', 'confidence': float, 'details': dict}
        """
        if not text or not isinstance(text, str):
            return {'language': 'unknown', 'confidence': 0.0, 'details': {}}
        
        # Очищаем текст
        cleaned_text = self._clean_text(text)
        
        # Если текст пустой после очистки
        if not cleaned_text:
            return {'language': 'unknown', 'confidence': 0.0, 'details': {}}
        
        # Разбиваем на слова
        words = cleaned_text.split()
        
        # Если нет слов
        if not words:
            return {'language': 'unknown', 'confidence': 0.0, 'details': {}}
        
        # Собираем все метрики
        ru_unique, uk_unique = self._count_unique_letters(cleaned_text)
        ru_freq, uk_freq = self._count_frequent_letters(cleaned_text)
        ru_endings, uk_endings = self._check_word_endings(words)
        ru_markers, uk_markers = self._check_marker_words(words)
        ru_digrams, uk_digrams = self._check_digrams(cleaned_text)
        
        # Рассчитываем взвешенные баллы для каждого языка
        scores = {
            'russian': (ru_unique * 2) + ru_freq + (ru_endings * 1.5) + (ru_markers * 3) + ru_digrams,
            'ukrainian': (uk_unique * 2) + uk_freq + (uk_endings * 1.5) + (uk_markers * 3) + uk_digrams
        }
        
        # Общая сумма баллов
        total_score = scores['russian'] + scores['ukrainian']
        
        # Определяем язык и уверенность
        if total_score == 0:
            return {'language': 'unknown', 'confidence': 0.0, 'details': {}}
        
        if scores['russian'] > scores['ukrainian']:
            confidence = scores['russian'] / total_score
            language = 'russian'
        else:
            confidence = scores['ukrainian'] / total_score
            language = 'ukrainian'
        
        # Создаем подробную информацию о результатах анализа
        details = {
            'metrics': {
                'unique_letters': {'russian': ru_unique, 'ukrainian': uk_unique},
                'frequent_letters': {'russian': ru_freq, 'ukrainian': uk_freq},
                'word_endings': {'russian': ru_endings, 'ukrainian': uk_endings},
                'marker_words': {'russian': ru_markers, 'ukrainian': uk_markers},
                'digrams': {'russian': ru_digrams, 'ukrainian': uk_digrams}
            },
            'scores': scores
        }
        
        return {
            'language': language,
            'confidence': confidence,
            'details': details
        }
        
    def analyze_text(self, text):
        """
        Проводит подробный анализ текста и возвращает все метрики.
        
        Args:
            text (str): Текст для анализа
            
        Returns:
            dict: Подробная информация о результатах анализа
        """
        if not text or not isinstance(text, str):
            return {'error': 'Empty or invalid text'}
            
        # Определяем язык
        result = self.get_confidence(text)
        
        # Определяем длину текста и количество слов
        cleaned_text = self._clean_text(text)
        words = cleaned_text.split() if cleaned_text else []
        
        # Добавляем базовую статистику
        result['stats'] = {
            'text_length': len(text),
            'cleaned_length': len(cleaned_text),
            'word_count': len(words),
            'average_word_length': sum(len(word) for word in words) / len(words) if words else 0
        }
        
        return result

# Пример использования
def main():
    detector = LangDetector()
    
    # Примеры текстов
    russian_text = "Это текст на русском языке с использованием ы, ъ и других букв. В русском языке есть особенности, которые отличают его от украинского."
    ukrainian_text = "Це текст українською мовою з використанням ї, і, є та інших літер. В українській мові є особливості, які відрізняють її від російської."
    
    # Тексты без явных признаков
    ambiguous_text = "Мама мыла раму. Она пошла домой."
    
    print(f"Русский текст определен как: {detector.detect_language(russian_text)}")
    print(f"Украинский текст определен как: {detector.detect_language(ukrainian_text)}")
    print(f"Неоднозначный текст определен как: {detector.detect_language(ambiguous_text)}")
    
    # С уверенностью
    print("\nРезультаты с уверенностью:")
    ru_result = detector.get_confidence(russian_text)
    uk_result = detector.get_confidence(ukrainian_text)
    am_result = detector.get_confidence(ambiguous_text)
    
    print(f"Русский текст: {ru_result['language']} (уверенность: {ru_result['confidence']:.2f})")
    print(f"Украинский текст: {uk_result['language']} (уверенность: {uk_result['confidence']:.2f})")
    print(f"Неоднозначный текст: {am_result['language']} (уверенность: {am_result['confidence']:.2f})")
    
    # Подробный анализ
    print("\nПодробный анализ русского текста:")
    analysis = detector.analyze_text(russian_text)
    print(f"Язык: {analysis['language']}")
    print(f"Уверенность: {analysis['confidence']:.2f}")
    print(f"Статистика: {analysis['stats']}")
    print(f"Метрики: {analysis['details']['metrics']}")
    
if __name__ == "__main__":
    main()
