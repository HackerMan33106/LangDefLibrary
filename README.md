# LangDefLib

Библиотека для определения языка текста без внешних зависимостей. Поддерживает различные славянские языки и английский язык.

## Особенности

- Определение языка текста без использования сторонних библиотек
- Встроенная поддержка русского, украинского, белорусского, польского и английского языков
- Возможность добавления собственных языков
- Подробный анализ текста с метриками
- Простой и удобный API
- Высокая скорость работы
- 100% Python без С-расширений
- Не требует подключения к интернету

## Установка

```bash
# Клонирование репозитория
git clone https://github.com/HackerMan33106/LangDefLib.git
cd LangDefLib

# Установка библиотеки
pip install -e .
```

## Быстрый старт

```python
from LangDefLib import LangDetector, detect_language

# Быстрое определение языка
result = detect_language("Это пример текста на русском языке")
print(result)  # {'language': 'russian', 'confidence': 0.95}

# Создание детектора для всех поддерживаемых языков
detector = LangDetector(languages=['russian', 'ukrainian', 'belarusian', 'english', 'polish'])

# Определение языка с использованием детектора
result = detector.detect("This is an example text in English")
print(result)  # {'language': 'english', 'confidence': 0.99}

# Получение подробного анализа
analysis = detector.analyze("Це приклад тексту українською мовою")
print(analysis)
```

## Подробное использование

### Класс LangDetector

Основной класс для определения языка текста.

```python
detector = LangDetector(
    languages=['russian', 'ukrainian'],  # Список языков для определения
    data_dir='path/to/data',  # Директория с данными языков (опционально)
    min_confidence=0.6  # Минимальный порог уверенности (опционально)
)
```

### Методы LangDetector

#### detect(text)

Определяет язык текста.

```python
result = detector.detect("Это пример текста на русском языке")
print(result)  # {'language': 'russian', 'confidence': 0.95}
```

#### detect_from_file(file_path)

Определяет язык текста из файла.

```python
result = detector.detect_from_file("path/to/text/file.txt")
print(result)  # {'language': 'russian', 'confidence': 0.95}
```

#### analyze(text)

Проводит подробный анализ текста.

```python
analysis = detector.analyze("Це приклад тексту українською мовою")
print(analysis)
```

Результат содержит:
- Определенный язык
- Уверенность определения
- Статистику текста (длина, количество слов и т.д.)
- Подробные метрики по каждому языку
- Топ наиболее вероятных языков

#### add_language(lang_code, data)

Добавляет новый язык для определения.

```python
detector.add_language('german', {
    'unique_letters': ['ä', 'ö', 'ü', 'ß'],
    'frequent_letters': ['ä', 'ö', 'ü', 'ß'],
    'word_endings': ['en', 'er', 'ung', 'ich', 'lich', 'ig', 'keit', 'heit', 'schaft'],
    'marker_words': ['und', 'oder', 'aber', 'der', 'die', 'das', 'in', 'mit', 'für', 'von', 'zu'],
    'digrams': ['ch', 'ck', 'ei', 'ie', 'sch', 'st', 'th'],
    'trigrams': ['sch', 'che', 'ein', 'ich', 'und', 'den'],
    'alphabet': 'abcdefghijklmnopqrstuvwxyzäöüß'
})
```

#### remove_language(lang_code)

Удаляет язык из списка определения.

```python
detector.remove_language('polish')
```

#### create_language_data_file(lang_code, data, output_dir)

Создает JSON-файл с данными о языке.

```python
detector.create_language_data_file('german', german_data, 'path/to/data')
```

### Вспомогательная функция detect_language

Для быстрого определения языка без создания экземпляра класса.

```python
from LangDefLib import detect_language

result = detect_language("This is a simple English text", languages=['english', 'russian'])
print(result)  # {'language': 'english', 'confidence': 0.99}
```

## Поддерживаемые языки

По умолчанию библиотека поддерживает следующие языки:
- Русский
- Украинский
- Белорусский
- Английский
- Польский

## Добавление своих языков

Для добавления нового языка создайте словарь с данными о языке:

```python
german_data = {
    'unique_letters': ['ä', 'ö', 'ü', 'ß'],
    'frequent_letters': ['ä', 'ö', 'ü', 'ß'],
    'word_endings': ['en', 'er', 'ung', 'ich', 'lich', 'ig', 'keit', 'heit', 'schaft'],
    'marker_words': ['und', 'oder', 'aber', 'der', 'die', 'das', 'in', 'mit', 'für', 'von', 'zu'],
    'digrams': ['ch', 'ck', 'ei', 'ie', 'sch', 'st', 'th'],
    'trigrams': ['sch', 'che', 'ein', 'ich', 'und', 'den'],
    'alphabet': 'abcdefghijklmnopqrstuvwxyzäöüß',
    'weights': {
        'unique_letters': 2.0,
        'frequent_letters': 1.0,
        'word_endings': 1.5,
        'marker_words': 3.0,
        'digrams': 1.0,
        'trigrams': 1.2
    }
}

detector.add_language('german', german_data)
```

Вы также можете сохранить данные в JSON-файл:

```python
detector.create_language_data_file('german', german_data)
```

## Лицензия

MIT

## Авторы

- [@HackerMan33106](https://github.com/HackerMan33106)

## Поддержка внешних библиотек

Библиотека также поддерживает интеграцию с внешними библиотеками определения языка:

- **fastText** - высокоточная библиотека от Facebook (поддерживает 176 языков)
- **langdetect** - простая и легкая библиотека

### Установка с поддержкой внешних библиотек

```bash
# Установка только основной библиотеки
pip install -e .

# Установка с поддержкой fastText
pip install -e ".[fasttext]"

# Установка с поддержкой langdetect
pip install -e ".[langdetect]"

# Установка с поддержкой всех внешних библиотек
pip install -e ".[all]"
```

### Использование fastText

fastText требует предварительно обученную модель для определения языка. Доступны две модели:
- Маленькая (917 КБ): [lid.176.ftz](https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz)
- Большая (126 МБ): [lid.176.bin](https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin)

Скачайте нужную модель и укажите путь к ней при использовании:

```bash
# Скачиваем модель
wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz
```

```python
from LangDefLib import ExternalDetector, detect_language_external

# Быстрое определение языка с помощью fastText
result = detect_language_external("Это пример текста", method='fasttext')
print(result)  # {'language': 'ru', 'confidence': 0.92}

# Использование детектора с указанием пути к модели
detector = ExternalDetector(fasttext_model_path='./lid.176.ftz')
result = detector.detect("This is an example text", method='fasttext')
print(result)  # {'language': 'en', 'confidence': 0.98}
```

### Сравнение методов

Можно использовать разные методы определения языка и сравнивать их результаты:

```python
from LangDefLib import ExternalDetector

detector = ExternalDetector()
text = "Привет, мир!"

# Определение языка с использованием всех методов
results = detector.detect_with_all_methods(text)

# Результаты всех методов
print(f"fastText: {results['fasttext']}")
print(f"langdetect: {results['langdetect']}")

# Лучший метод
print(f"Лучший метод: {results['best_method']} -> {results['best']['language']}")
```

### Голосование методов

Для повышения точности можно использовать голосование всех методов:

```python
from LangDefLib import ExternalDetector

detector = ExternalDetector()
text = "Привет, мир!"

# Определение языка с использованием голосования
result = detector.detect(text, method='vote')
print(f"Язык: {result['language']}")
print(f"Уверенность: {result['confidence']}")
print(f"Голосов: {result['votes']}/{result['total_votes']}")
```

### Преимущества разных методов

- **fastText**: наиболее точный метод, поддерживает 176 языков, работает хорошо с текстами среднего и большого размера
- **langdetect**: простой и легкий метод, не требует дополнительных моделей

Для коротких текстов (1-2 слова) рекомендуется использовать голосование всех методов. 