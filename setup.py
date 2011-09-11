#!/usr/bin/env python

from __future__ import with_statement

import os
from setuptools import setup, find_packages


def read_file(name):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(dir_name, name)
    with open(file_name) as f_obj:
        return f_obj.read()


setup(
    name = 'collapsar',
    version = '0.01',
    description = 'Python ioc container',
    author = 'Karataev Pavel',
    author_email = 'minmax777@gmail.com',
    url = 'https://github.com/minmax/collapsar',
    license = read_file('UNLICENSE'),
    packages = find_packages(exclude=['tests', 'tests.*']),
    package_data = {'collapsar': ["README", "UNLICENSE"]},
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: OS Independent',
    ]
)
