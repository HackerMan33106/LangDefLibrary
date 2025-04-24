#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LangDefLib - библиотека для определения языка текста без внешних зависимостей.
"""

from .LangDefLib import LangDetector, detect_language, main

# Импортируем функциональность внешних библиотек (будет работать, только если установлены библиотеки)
try:
    from .external import ExternalDetector, detect_language_external, get_language
    __all__ = ['LangDetector', 'detect_language', 'main', 'ExternalDetector', 'detect_language_external', 'get_language']
except ImportError:
    __all__ = ['LangDetector', 'detect_language', 'main']

__version__ = '1.0.0' 