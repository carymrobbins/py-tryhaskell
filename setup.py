#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="tryhaskell",
    version="0.1.0",
    author="Cary Robbins",
    author_email="carymrobbins@gmail.com",
    url="{{homepage}}",
    packages=["tryhaskell"],
    description="Python client for tryhaskell.org",
    long_description=open('README.rst').read(),
    license=open('LICENSE').read(),
    install_requires=[
        'requests==2.3.0',
    ],
    classifiers=[
    ]
)
