#!/usr/bin/env python
from setuptools import setup, find_packages
import os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

entry_points = """
[zc.buildout]
install=lovely.recipe.cappuccino.install:Install
builder=lovely.recipe.cappuccino.builder:Builder
"""

setup (
    name='lovely.recipe.cappuccino',
    description = "local cappuccino setup for zc.buildout",
    long_description=(
        read('README.rst')
        + '\n\n' +
        read('CHANGES.txt')
        ),
    version='0.0.2',
    author = "Lovely Systems",
    author_email = "office@lovelysystems.com",
    license = "ZPL 2.1",
    keywords = "buildout recipe cappuccino javascript objectiv-j cocoa",
    url = 'http://github.com/lovelysystems/lovely.recipe.cappuccino',
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
    entry_points = entry_points,
    zip_safe = False,
    )

