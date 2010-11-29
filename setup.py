#!/usr/bin/env python
from setuptools import setup, find_packages
import os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup (
    name='lovely.recipe.cappuccino',
    description = "local cappuccino setup for zc.buildout",
    long_description=(
        read('README.txt')
        + '\n\n' +
        'Detailed Documentation\n'
        '**********************'
        + '\n\n' +
        read('src', 'lovely', 'recipe', 'cappuccino', 'README.txt')
        + '\n\n' +
        read('CHANGES.txt')
        ),
    version='0.0.0a1',
    author = "Lovely Systems",
    author_email = "office@lovelysystems.com",
    license = "ZPL 2.1",
    keywords = "buildout recipe cappuccino javascript objectiv-j cocoa",
    url = 'http://github.org/lovelysystems/lovely.recipe.cappuccino',
    packages = find_packages('src'),
    include_package_data = True,
    package_dir = {'':'src'},
    namespace_packages = ['lovely', 'lovely.recipe',],
    extras_require = dict(
                    test=[
                        'zope.testing',
                        ]),
    install_requires = ['setuptools',
                        'zc.buildout',
                        ],
    entry_points = {'zc.buildout':
                    ['default = lovely.recipe.cappuccino.build:Install']},
    zip_safe = True,
    )

