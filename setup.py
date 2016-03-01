#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Based on https://github.com/pypa/sampleproject
See: https://packaging.python.org/en/latest/distributing.html
"""

# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sieve-git-pushdeploy',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1.0',

    description='Push a sieve script to your mailserver and have it applied automatically.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/mheistermann/sieve-git-pushdeploy',

    # Author details
    author='Martin Heistermann',
    author_email='sieve-git-pushdeploy@mheistermann.de',

    # Choose your license
    license='GPLv3+',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2 :: Only', # :( need to upgrade dependencies
        'Programming Language :: Python :: 2.7',
    ],
    keywords='git sieve pushdeployment',

    py_modules=["hooks"],
    install_requires=['sievelib'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    #extras_require={
    #    'dev': ['check-manifest'],
    #    'test': ['coverage'],
    #},

    entry_points={
        'console_scripts': [
            'sieve-git-pushdeploy=hooks:main',
        ],
    },
)
