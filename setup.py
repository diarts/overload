import pathlib
from setuptools import setup, find_packages

# Current dir.
HOME = pathlib.Path(__file__).parent

# Short description.
DESCRIPTION = (
    'Python3 function overload lib, based on pure python and native typing.'
)

# Text of README.md file.
README_TEXT = HOME / 'README.md'
README_TEXT = README_TEXT.read_text()

setup(
    name='overloader',
    version='0.1.1',
    description=DESCRIPTION,
    long_description=README_TEXT,
    long_description_content_type='text/markdown',
    url='https://github.com/diarts/overload',
    author='diarts',
    author_email='diarts@mail.ru',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    package_dir={"": "."},
    packages=[
        "overload",
        "overload.decorator",
        "overload.exception",
        "overload.implementation",
        "overload.overloader",
        "overload.type",
        "overload.utils",
    ],
    python_requires=">=3.7",
)
