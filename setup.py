from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='SellsyAPI',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='@mlabarrere',
    description='A Python library to interact with the Sellsy API',
    long_description=long_description,
    keywords='sellsy api client',
    url='https://github.com/O-clock-Dev/SellsyAPI'
)
