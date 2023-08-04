from setuptools import setup, find_packages

# Refer to the official Python Packaging Authority (PyPA) documentation for more details: https://packaging.python.org/tutorials/packaging-projects/
setup(
    name='tt_test_api_2_0',
    version='0.1.0',
    author='Isaac Manuel',
    author_email='',
    description='An client for the Trading Technologies Rest API 2.0',
    packages=find_packages(),  # Automatically find all packages in the project
    install_requires=[
        'requests', 'logging', 'uuid', 'abc'
        # List your library's dependencies here
    ],
)