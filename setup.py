#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="LangDefLib",
    version="1.0.0",
    author="abobu",
    author_email="your.email@example.com",
    description="Библиотека для определения языка текста без внешних зависимостей",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HackerMan33106/LangDefLib",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Russian",
        "Natural Language :: Ukrainian",
        "Natural Language :: English",
        "Natural Language :: Polish",
        "Natural Language :: Belarusian",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    package_data={
        "LangDefLib": ["data/*.json"],
    },
    extras_require={
        "fasttext": ["fasttext-wheel>=0.9.2"],
        "langdetect": ["langdetect>=1.0.9"],
        "all": ["fasttext-wheel>=0.9.2", "langdetect>=1.0.9"],
    },
    entry_points={
        "console_scripts": [
            "langdeflib=LangDefLib:main",
        ],
    },
) 