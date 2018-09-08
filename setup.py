#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

from setuptools import setup
import os.path

setup(
    name = 'gpc',
    version = '1',
    author = 'Mordae',
    description = ('CSV, TXT To GPC Conversion Web Service'),
    license = 'MIT',
    keywords = 'csv gpc',
    url = 'http://gpc.mordae.eu/',
    include_package_data = True,
    package_data = {
        '': ['*.png', '*.js', '*.png', '*.html'],
    },
    packages = [
        'mordae',
        'mordae.gpc',
    ],
    classifiers = [
        'License :: OSI Approved :: MIT License',
    ],
    scripts = ['gpc']
)


# vim:set sw=4 ts=4 et:
