#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="tryhaskell",
    version=__import__('tryhaskell').__version__,
    author="Cary Robbins",
    author_email="carymrobbins@gmail.com",
    url="https://github.com/carymrobbins/py-tryhaskell",
    packages=find_packages(),
    description="Python client for tryhaskell.org",
    license='BSD3',
    install_requires=[
        'requests',
    ],
    classifiers=[
    ]
)
