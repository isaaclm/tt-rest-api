from setuptools import setup, find_packages

# Refer to the official Python Packaging Authority (PyPA) documentation for more details: https://packaging.python.org/tutorials/packaging-projects/
setup(
    name='tt-rest-api',
    version='0.1.0',
    author='Isaac',
    description='An client for the Trading Technologies Rest API 2.0',
    url='https://github.com/isaaclm/tt-rest-api',
    packages=['ttrest'],
    package_dir={'ttrest': 'ttrest'},
    install_requires=[
        'requests', 'logging', 'uuid', 'datetime'
    ],
)