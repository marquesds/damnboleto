import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'pdftotext==2.0.1'
]

dependencies = [
]

setup(
    name='damnboleto',
    version='1.0.0',
    description='Extract boleto\'s data',
    classifiers=[
        'Programming Language :: Python :: 3.6'
    ],
    author='Lucas Marques',
    author_email='lucasmarquesds@gmail.com',
    url='',
    keywords='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    dependency_links=dependencies
)
