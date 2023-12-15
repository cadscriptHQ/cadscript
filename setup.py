from setuptools import setup, find_packages

setup(
    name='cadscript',
    version='0.2',
    author='Andreas Kahler',
    author_email='mail@andreaskahler.com',
    packages=find_packages(),
    install_requires=[
        'cadquery'
    ],
)
