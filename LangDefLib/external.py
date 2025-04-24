#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль для интеграции с внешними библиотеками определения языка.
Поддерживает fastText и langdetect.
"""

import os
import warnings
import logging
from typing import Dict, Any, List, Optional, Union, Tuple, Set

# Настройка логирования
logger = logging.getLogger(__name__)


class ExternalDetector:
    """
    Класс для определения языка с использованием внешних библиотек.
    Поддерживает fastText и langdetect.
    """
    
    def __init__(
        self, 
        use_fasttext: bool = True, 
        use_langdetect: bool = True,
        fasttext_model_path: Optional[str] = None,
        fasttext_model_size: str = 'small',
        min_confidence: float = 0.5,
        log_level: int = logging.WARNING
    ):
        """
        Инициализирует детектор с указанными внешними библиотеками.
        
        Args:
            use_fasttext (bool): Использовать fastText для определения языка
            use_langdetect (bool): Использовать langdetect для определения языка
            fasttext_model_path (str, optional): Путь к модели fastText
            fasttext_model_size (str): Размер модели fastText ('small' или 'big')
            min_confidence (float): Минимальная уверенность для определения языка
            log_level (int): Уровень логирования (по умолчанию WARNING)
        """
        # Настройка логирования
        logging.basicConfig(level=log_level)
        
        self.use_fasttext = use_fasttext
        self.use_langdetect = use_langdetect
        self.min_confidence = min_confidence
        
        # Инициализируем библиотеки
        self.fasttext_model = None
        self.langdetect_module = None
        
        # Загружаем библиотеки, если указано
        if self.use_fasttext:
            self._load_fasttext(fasttext_model_path, fasttext_model_size)
        
        if self.use_langdetect:
            self._load_langdetect()
        
        # Проверяем, что хотя бы одна библиотека загружена
        if not (self.use_fasttext or self.use_langdetect):
            logger.warning(
                "Ни одна из библиотек определения языка не загружена. "
                "Детектор будет возвращать 'unknown' для всех текстов."
            )
    
    def _load_fasttext(self, model_path: Optional[str], model_size: str = 'small') -> None:
        """
        Загружает модель fastText для определения языка.
        
        Args:
            model_path (str, optional): Путь к модели fastText
            model_size (str): Размер модели fastText ('small' или 'big')
        """
        try:
            # Попытка импортировать fasttext-wheel
            try:
                import fasttext
                logger.info("Используется fasttext-wheel")
            except ImportError:
                try:
                    import fasttext
                    logger.info("Используется fasttext")
                except ImportError:
                    raise ImportError("Не удалось импортировать fasttext. Установите: pip install fasttext-wheel")
            
            # Если путь не указан, используем стандартные пути к моделям
            if model_path is None:
                if model_size == 'small':
                    model_name = 'lid.176.ftz'
                else:
                    model_name = 'lid.176.bin'
                
                # Ищем модель в текущей директории, директории библиотеки и директории проекта
                possible_paths = [
                    model_name,
                    os.path.join(os.path.dirname(os.path.abspath(__file__)), model_name),
                    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), model_name)
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        model_path = path
                        break
            
            # Если модель найдена, загружаем её
            if model_path and os.path.exists(model_path):
                try:
                    self.fasttext_model = fasttext.load_model(model_path)
                    logger.info(f"Модель fastText успешно загружена из {model_path}")
                except Exception as e:
                    logger.error(f"Ошибка при загрузке модели fastText: {e}")
                    self.use_fasttext = False
            else:
                warnings.warn(
                    f"Модель fastText не найдена. Для использования fastText скачайте модель "
                    f"с https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz (маленькая) "
                    f"или https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin (большая) "
                    f"и укажите путь к ней в параметре fasttext_model_path."
                )
                self.use_fasttext = False
        except ImportError as e:
            warnings.warn(
                f"Ошибка при импорте fastText: {e}. Для использования fastText установите: "
                "pip install fasttext-wheel"
            )
            self.use_fasttext = False
    
    def _load_langdetect(self) -> None:
        """
        Загружает библиотеку langdetect для определения языка.
        """
        try:
            import langdetect
            self.langdetect_module = langdetect
            logger.info("Библиотека langdetect успешно загружена")
            
            # Устанавливаем seed для воспроизводимости результатов
            try:
                langdetect.DetectorFactory.seed = 0
            except:
                logger.warning("Не удалось установить seed для langdetect")
                
        except ImportError:
            warnings.warn(
                "Библиотека langdetect не установлена. Для использования langdetect установите её: "
                "pip install langdetect"
            )
            self.use_langdetect = False
    
    def detect_fasttext(self, text: str, k: int = 1) -> List[Dict[str, Any]]:
        """
        Определяет язык текста с использованием fastText.
        
        Args:
            text (str): Текст для анализа
            k (int): Количество возвращаемых языков
            
        Returns:
            List[Dict[str, Any]]: Список языков с уверенностью определения
        """
        if not self.use_fasttext or not self.fasttext_model:
            return []
        
        # Обрабатываем пустой или слишком короткий текст
        if not text or len(text.strip()) < 3:
            logger.debug("Текст слишком короткий для fastText")
            return []
        
        try:
            # Получаем предсказания модели
            labels, scores = self.fasttext_model.predict(text, k=k)
            
            # Обрабатываем результаты
            results = []
            for i in range(len(labels)):
                if i < len(scores):
                    # Извлекаем язык из метки (__label__ru -> ru)
                    lang = labels[i].replace('__label__', '')
                    confidence = float(scores[i])
                    
                    # Добавляем язык, только если уверенность выше порога
                    if confidence >= self.min_confidence:
                        results.append({
                            'language': lang,
                            'confidence': confidence
                        })
            
            return results
        except Exception as e:
            logger.error(f"Ошибка при определении языка с fastText: {e}")
            return []
    
    def detect_langdetect(self, text: str) -> List[Dict[str, Any]]:
        """
        Определяет язык текста с использованием langdetect.
        
        Args:
            text (str): Текст для анализа
            
        Returns:
            List[Dict[str, Any]]: Список языков с уверенностью определения
        """
        if not self.use_langdetect or not self.langdetect_module:
            return []
        
        # Обрабатываем пустой или слишком короткий текст
        if not text or len(text.strip()) < 10:  # langdetect требует больше текста
            logger.debug("Текст слишком короткий для langdetect")
            return []
        
        try:
            # Определяем язык с помощью langdetect
            result = self.langdetect_module.detect(text)
            
            # Используем langdetect.detect_langs для получения вероятностей
            probabilities = self.langdetect_module.detect_langs(text)
            confidence = 0.0
            
            # Ищем вероятность для определенного языка
            for prob in probabilities:
                if prob.lang == result:
                    confidence = prob.prob
                    break
            
            return [{
                'language': result,
                'confidence': confidence
            }]
        except Exception as e:
            logger.debug(f"Ошибка при определении языка с langdetect: {e}")
            return []
    
    def detect(self, text: str, method: str = 'all') -> Dict[str, Any]:
        """
        Определяет язык текста с использованием указанного метода.
        
        Args:
            text (str): Текст для анализа
            method (str): Метод определения языка: 'fasttext', 'langdetect', 'vote', 'all'
            
        Returns:
            Dict[str, Any]: Словарь с языком и уверенностью определения
        """
        if not text or not isinstance(text, str) or len(text.strip()) < 3:
            return {'language': 'unknown', 'confidence': 0.0, 'method': method}
        
        # Выбираем метод определения
        if method == 'fasttext':
            if not self.use_fasttext:
                return {'language': 'unknown', 'confidence': 0.0, 'method': 'fasttext'}
            
            results = self.detect_fasttext(text)
            if results:
                result = results[0]
                return {
                    'language': result['language'],
                    'confidence': result['confidence'],
                    'method': 'fasttext'
                }
            else:
                return {'language': 'unknown', 'confidence': 0.0, 'method': 'fasttext'}
        
        elif method == 'langdetect':
            if not self.use_langdetect:
                return {'language': 'unknown', 'confidence': 0.0, 'method': 'langdetect'}
            
            results = self.detect_langdetect(text)
            if results:
                result = results[0]
                return {
                    'language': result['language'],
                    'confidence': result['confidence'],
                    'method': 'langdetect'
                }
            else:
                return {'language': 'unknown', 'confidence': 0.0, 'method': 'langdetect'}
        
        elif method == 'vote':
            return self._vote_language(text)
        
        elif method == 'all':
            return self._detect_all(text)
        
        else:
            logger.warning(f"Неизвестный метод: {method}. Используется метод 'vote'.")
            return self._vote_language(text)
    
    def _vote_language(self, text: str) -> Dict[str, Any]:
        """
        Определяет язык голосованием всех доступных методов.
        
        Args:
            text (str): Текст для анализа
            
        Returns:
            Dict[str, Any]: Словарь с языком и уверенностью определения
        """
        votes = {}
        method_results = {}
        
        # Получаем результаты от всех доступных методов
        if self.use_fasttext:
            ft_results = self.detect_fasttext(text, k=1)
            if ft_results:
                lang = ft_results[0]['language']
                conf = ft_results[0]['confidence']
                votes[lang] = votes.get(lang, 0) + conf
                method_results['fasttext'] = {'language': lang, 'confidence': conf}
        
        if self.use_langdetect:
            ld_results = self.detect_langdetect(text)
            if ld_results:
                lang = ld_results[0]['language']
                conf = ld_results[0]['confidence']
                votes[lang] = votes.get(lang, 0) + conf
                method_results['langdetect'] = {'language': lang, 'confidence': conf}
        
        # Если нет голосов, возвращаем неизвестный язык
        if not votes:
            return {'language': 'unknown', 'confidence': 0.0, 'method': 'vote'}
        
        # Находим лучший язык по голосам
        best_lang = max(votes.items(), key=lambda x: x[1])
        language = best_lang[0]
        
        # Считаем среднюю уверенность для лучшего языка
        confidence_sum = 0.0
        num_methods = 0
        
        for method, result in method_results.items():
            if result['language'] == language:
                confidence_sum += result['confidence']
                num_methods += 1
        
        # Если нет совпадений, берем уверенность из голосов
        if num_methods == 0:
            confidence = best_lang[1] / sum(votes.values())
        else:
            confidence = confidence_sum / num_methods
        
        return {
            'language': language,
            'confidence': confidence,
            'method': 'vote',
            'methods_used': list(method_results.keys())
        }
    
    def _detect_all(self, text: str) -> Dict[str, Any]:
        """
        Определяет язык всеми доступными методами и возвращает лучший результат.
        
        Args:
            text (str): Текст для анализа
            
        Returns:
            Dict[str, Any]: Словарь с языком и уверенностью определения
        """
        results = {}
        
        # Получаем результаты от всех методов
        if self.use_fasttext:
            results['fasttext'] = self.detect(text, method='fasttext')
        
        if self.use_langdetect:
            results['langdetect'] = self.detect(text, method='langdetect')
        
        # Добавляем результат голосования
        results['vote'] = self._vote_language(text)
        
        # Находим метод с наивысшей уверенностью
        best_method = None
        best_confidence = -1
        
        for method, result in results.items():
            if result['confidence'] > best_confidence:
                best_confidence = result['confidence']
                best_method = method
        
        # Если нет лучшего метода, возвращаем неизвестный язык
        if best_method is None:
            return {'language': 'unknown', 'confidence': 0.0, 'method': 'all', 'best_method': None}
        
        results['best'] = results[best_method]
        results['best_method'] = best_method
        
        return results
    
    def detect_with_all_methods(self, text: str) -> Dict[str, Any]:
        """
        Определяет язык всеми доступными методами и возвращает все результаты.
        
        Args:
            text (str): Текст для анализа
            
        Returns:
            Dict[str, Any]: Словарь с результатами всех методов
        """
        results = {}
        
        # Получаем результаты от всех методов
        if self.use_fasttext:
            results['fasttext'] = self.detect(text, method='fasttext')
        
        if self.use_langdetect:
            results['langdetect'] = self.detect(text, method='langdetect')
        
        # Добавляем результат голосования
        results['vote'] = self._vote_language(text)
        
        # Находим метод с наивысшей уверенностью
        best_method = None
        best_confidence = -1
        
        for method, result in results.items():
            if result['confidence'] > best_confidence and result['language'] != 'unknown':
                best_confidence = result['confidence']
                best_method = method
        
        # Если нет лучшего метода, возвращаем неизвестный язык
        if best_method is None:
            best_method = 'vote'
        
        results['best'] = results[best_method]
        results['best_method'] = best_method
        
        return results
    
    def get_top_languages(self, text: str, n: int = 3) -> List[Dict[str, Any]]:
        """
        Получает список наиболее вероятных языков для текста.
        
        Args:
            text (str): Текст для анализа
            n (int): Количество языков в результате
            
        Returns:
            List[Dict[str, Any]]: Список языков с уверенностью определения
        """
        if not text or not isinstance(text, str) or len(text.strip()) < 3:
            return [{'language': 'unknown', 'confidence': 0.0, 'method': 'all'}]
        
        # Список всех предсказаний от разных методов
        all_predictions = []
        
        # Добавляем результаты fastText (до n языков)
        if self.use_fasttext:
            try:
                ft_results = self.detect_fasttext(text, k=n)
                for result in ft_results:
                    all_predictions.append({
                        'language': result['language'],
                        'confidence': result['confidence'],
                        'method': 'fasttext'
                    })
            except Exception as e:
                logger.debug(f"Ошибка при получении топ языков с fastText: {e}")
        
        # Добавляем результат langdetect
        if self.use_langdetect:
            try:
                ld_results = self.detect_langdetect(text)
                for result in ld_results:
                    all_predictions.append({
                        'language': result['language'],
                        'confidence': result['confidence'],
                        'method': 'langdetect'
                    })
            except Exception as e:
                logger.debug(f"Ошибка при получении топ языков с langdetect: {e}")
        
        # Если нет предсказаний, возвращаем неизвестный язык
        if not all_predictions:
            return [{'language': 'unknown', 'confidence': 0.0, 'method': 'all'}]
        
        # Группируем предсказания по языку и находим среднюю уверенность
        language_scores = {}
        
        for pred in all_predictions:
            lang = pred['language']
            conf = pred['confidence']
            method = pred['method']
            
            if lang not in language_scores:
                language_scores[lang] = {
                    'sum': conf,
                    'count': 1,
                    'methods': [method]
                }
            else:
                language_scores[lang]['sum'] += conf
                language_scores[lang]['count'] += 1
                language_scores[lang]['methods'].append(method)
        
        # Создаем список языков с усредненной уверенностью
        languages = []
        
        for lang, data in language_scores.items():
            avg_confidence = data['sum'] / data['count']
            methods = ', '.join(set(data['methods']))
            
            languages.append({
                'language': lang,
                'confidence': avg_confidence,
                'method': methods
            })
        
        # Сортируем по уверенности и ограничиваем количество результатов
        languages.sort(key=lambda x: x['confidence'], reverse=True)
        
        return languages[:n]
    
    def get_language(self, text: str, method: str = 'all') -> str:
        """
        Определяет язык текста и возвращает только код языка без дополнительной информации.
        
        Args:
            text (str): Текст для анализа
            method (str): Метод определения языка: 'fasttext', 'langdetect', 'vote', 'all'
            
        Returns:
            str: Код языка ('en', 'ru', 'uk', ...) или 'unknown'
        """
        result = self.detect(text, method=method)
        return result.get('language', 'unknown')


def detect_language_external(
    text: str, 
    method: str = 'all',
    use_fasttext: bool = True,
    use_langdetect: bool = True,
    fasttext_model_path: Optional[str] = None,
    min_confidence: float = 0.5
) -> Dict[str, Any]:
    """
    Вспомогательная функция для быстрого определения языка текста с внешними библиотеками.
    
    Args:
        text (str): Текст для анализа
        method (str): Метод определения языка: 'fasttext', 'langdetect', 'vote', 'all'
        use_fasttext (bool): Использовать fastText для определения языка
        use_langdetect (bool): Использовать langdetect для определения языка
        fasttext_model_path (str, optional): Путь к модели fastText
        min_confidence (float): Минимальная уверенность для определения языка
        
    Returns:
        Dict[str, Any]: Словарь с языком и уверенностью определения
    """
    detector = ExternalDetector(
        use_fasttext=use_fasttext,
        use_langdetect=use_langdetect,
        fasttext_model_path=fasttext_model_path,
        min_confidence=min_confidence
    )
    
    return detector.detect(text, method=method)


def get_language(
    text: str, 
    method: str = 'all',
    use_fasttext: bool = True,
    use_langdetect: bool = True,
    fasttext_model_path: Optional[str] = None,
    min_confidence: float = 0.5
) -> str:
    """
    Вспомогательная функция для быстрого определения языка текста,
    возвращающая только код языка.
    
    Args:
        text (str): Текст для анализа
        method (str): Метод определения языка: 'fasttext', 'langdetect', 'vote', 'all'
        use_fasttext (bool): Использовать fastText для определения языка
        use_langdetect (bool): Использовать langdetect для определения языка
        fasttext_model_path (str, optional): Путь к модели fastText
        min_confidence (float): Минимальная уверенность для определения языка
        
    Returns:
        str: Код языка ('en', 'ru', 'uk', ...) или 'unknown'
    """
    detector = ExternalDetector(
        use_fasttext=use_fasttext,
        use_langdetect=use_langdetect,
        fasttext_model_path=fasttext_model_path,
        min_confidence=min_confidence
    )
    
    return detector.get_language(text, method=method)


def get_supported_languages() -> Dict[str, Set[str]]:
    """
    Возвращает список языков, поддерживаемых каждой библиотекой.
    
    Returns:
        Dict[str, Set[str]]: Словарь с списками языков для каждой библиотеки
    """
    languages = {
        'fasttext': set(),
        'langdetect': set()
    }
    
    # Языки fastText (176 языков)
    try:
        languages['fasttext'] = {
            'ab', 'ace', 'ady', 'af', 'ak', 'als', 'am', 'an', 'ang', 'ar', 'arc',
            'arz', 'as', 'ast', 'av', 'ay', 'az', 'ba', 'bar', 'bcl', 'be', 'bg',
            'bh', 'bi', 'bjn', 'bm', 'bn', 'bo', 'bpy', 'br', 'bs', 'bxr', 'ca',
            'cbk', 'ce', 'ceb', 'ch', 'chr', 'chy', 'co', 'cr', 'crh', 'cs', 'csb',
            'cu', 'cv', 'cy', 'da', 'de', 'diq', 'dsb', 'dty', 'dv', 'dz', 'ee',
            'el', 'en', 'eo', 'es', 'et', 'eu', 'ext', 'fa', 'ff', 'fi', 'fj', 'fo',
            'fr', 'frp', 'frr', 'fur', 'fy', 'ga', 'gag', 'gan', 'gd', 'gl', 'glk',
            'gn', 'gom', 'got', 'gu', 'gv', 'ha', 'hak', 'haw', 'he', 'hi', 'hif',
            'ho', 'hr', 'hsb', 'ht', 'hu', 'hy', 'ia', 'id', 'ie', 'ig', 'ik', 'ilo',
            'io', 'is', 'it', 'iu', 'ja', 'jam', 'jbo', 'jv', 'ka', 'kaa', 'kab',
            'kbd', 'kbp', 'kg', 'ki', 'kj', 'kk', 'kl', 'km', 'kn', 'ko', 'koi',
            'kr', 'krc', 'ks', 'ksh', 'ku', 'kv', 'kw', 'ky', 'la', 'lad', 'lb',
            'lbe', 'lez', 'lfn', 'lg', 'li', 'lij', 'lmo', 'ln', 'lo', 'lt', 'ltg',
            'lv', 'mai', 'mdf', 'mg', 'mh', 'mhr', 'mi', 'min', 'mk', 'ml', 'mn',
            'mr', 'mrj', 'ms', 'mt', 'mus', 'mwl', 'my', 'myv', 'mzn', 'na', 'nah',
            'nap', 'nds', 'ne', 'new', 'ng', 'nl', 'nn', 'no', 'nov', 'nrm', 'nso',
            'nv', 'ny', 'oc', 'olo', 'om', 'or', 'os', 'pa', 'pag', 'pam', 'pap',
            'pcd', 'pdc', 'pfl', 'pi', 'pih', 'pl', 'pms', 'pnb', 'pnt', 'ps', 'pt',
            'qu', 'rm', 'rmy', 'rn', 'ro', 'ru', 'rue', 'rw', 'sa', 'sah', 'sc',
            'scn', 'sco', 'sd', 'se', 'sg', 'sh', 'si', 'sk', 'sl', 'sm', 'sn', 'so',
            'sq', 'sr', 'srn', 'ss', 'st', 'stq', 'su', 'sv', 'sw', 'szl', 'ta', 'tcy',
            'te', 'tet', 'tg', 'th', 'ti', 'tk', 'tl', 'tn', 'to', 'tpi', 'tr', 'ts',
            'tt', 'tum', 'tw', 'ty', 'tyv', 'udm', 'ug', 'uk', 'ur', 'uz', 've', 'vec',
            'vep', 'vi', 'vls', 'vo', 'wa', 'war', 'wo', 'wuu', 'xal', 'xh', 'xmf',
            'yi', 'yo', 'za', 'zea', 'zh', 'zu'
        }
    except Exception:
        pass
    
    # Языки langdetect (55 языков)
    try:
        languages['langdetect'] = {
            'af', 'ar', 'bg', 'bn', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'es',
            'et', 'fa', 'fi', 'fr', 'gu', 'he', 'hi', 'hr', 'hu', 'id', 'it', 'ja',
            'kn', 'ko', 'lt', 'lv', 'mk', 'ml', 'mr', 'ne', 'nl', 'no', 'pa', 'pl',
            'pt', 'ro', 'ru', 'sk', 'sl', 'so', 'sq', 'sv', 'sw', 'ta', 'te', 'th',
            'tl', 'tr', 'uk', 'ur', 'vi', 'zh-cn', 'zh-tw'
        }
    except Exception:
        pass
    
    return languages


# Пример использования
def main():
    import sys
    
    # Создаем детектор
    detector = ExternalDetector()
    
    # Если есть аргументы, используем их как текст
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
    else:
        # Примеры текстов
        texts = [
            "This is an example text in English language.",
            "Это пример текста на русском языке.",
            "Це приклад тексту українською мовою.",
            "To jest przykładowy tekst w języku polskim.",
            "Dies ist ein Beispieltext in deutscher Sprache."
        ]
        
        print("Определение языка для примеров текста:")
        for text in texts:
            result = detector.detect(text)
            print(f"Текст: {text[:30]}...")
            print(f"Язык: {result['language']}, уверенность: {result['confidence']:.2f}")
            print()
        
        return
    
    # Определяем язык
    print(f"Текст: {text}")
    
    # Используем все методы
    results = detector.detect_with_all_methods(text)
    
    print("Результаты определения языка:")
    
    # fastText
    if 'fasttext' in results:
        ft_result = results['fasttext']
        print(f"fastText: {ft_result['language']} (уверенность: {ft_result['confidence']:.2f})")
    
    # langdetect
    if 'langdetect' in results:
        ld_result = results['langdetect']
        print(f"langdetect: {ld_result['language']} (уверенность: {ld_result['confidence']:.2f})")
    
    # Голосование
    vote_result = results['vote']
    print(f"Голосование: {vote_result['language']} (уверенность: {vote_result['confidence']:.2f})")
    
    # Лучший метод
    best_result = results['best']
    best_method = results['best_method']
    print(f"Лучший результат ({best_method}): {best_result['language']} (уверенность: {best_result['confidence']:.2f})")
    
    # Топ языков
    print("\nТоп-3 языка:")
    top_langs = detector.get_top_languages(text, n=3)
    for i, lang_info in enumerate(top_langs, 1):
        print(f"{i}. {lang_info['language']} (уверенность: {lang_info['confidence']:.2f}, метод: {lang_info['method']})")
    

if __name__ == "__main__":
    main() 