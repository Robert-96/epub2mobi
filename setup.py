from setuptools import setup, find_packages

from epub2mobi.__version__ import VERSION


NAME = 'epub2mobi'
DESCRIPTION = 'Simple script that converts all the epub files in a directory tree to mobi.'
URL = 'https://github.com/Robert-96/epub2mobi'
EMAIL = 'dezmereanrobert@gmail.com'
AUTHOR = 'Robert96'
REQUIRES_PYTHON = '>=3.6.0'
LICENSE = 'GNU GPLv3'


with open('requirements.txt') as fp:
    REQUIRED = fp.read().splitlines()


with open('README.md') as fp:
    README = fp.read()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type='text/markdown',
    license=LICENSE,
    url=URL,
    project_urls={
        "Bug Tracker": "https://github.com/Robert-96/epub2mobi/issues",
        "Documentation": "https://github.com/Robert-96/epub2mobi",
        "Source": "https://github.com/Robert-96/epub2mobi",
    },

    author=AUTHOR,
    author_email=EMAIL,

    python_requires=REQUIRES_PYTHON,
    setup_requires=REQUIRED,
    install_requires=REQUIRED,
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'epub2mobi = epub2mobi.cli:cli',
        ],
    },

    classifiers=[
        "Development Status :: 5 - Production/Stable",

        "Intended Audience :: Developers",
        "Intended Audience :: Other Audience",

        "Environment :: Console",

        "License :: OSI Approved :: MIT",

        "Programming Language :: Cython",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",

        "Operating System :: OS Independent",
    ],
    keywords="epub mobi e-books",
)