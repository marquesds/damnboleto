import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'pdftotext==2.1.12'
]

dependencies = [
]

setup(
    name='damnboleto',
    version='0.3.0',
    description='Extract boleto\'s data',
    classifiers=[
        'Programming Language :: Python :: 3.6'
    ],
    author='Lucas Marques',
    author_email='lucasmarquesds@gmail.com',
    url='https://github.com/marquesds/damnboleto',
    download_url='https://github.com/marquesds/damnboleto/archive/0.3.0.zip',
    keywords=['boleto', 'extractor', 'pdf'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    dependency_links=dependencies
)
