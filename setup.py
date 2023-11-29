from setuptools import setup, find_packages

setup(
    name='SellsyAPI',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='@mlabarrere',
    description='A Python library to interact with the Sellsy API',
    keywords='sellsy api client',
    url='https://github.com/O-clock-Dev/SellsyAPI'
)
