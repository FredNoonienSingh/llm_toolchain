"""Setup script """
# pylint: disable=E0401
from setuptools import setup, find_packages

with open("README.md", 'r', encoding='UTF-8') as f:
    long_description = f.read()

setup(
    name='llmtoolchain',
    version='1.0',
    description='a simple toolchain',
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Frederic Baumeister',
    author_email='FredBaumeister@Icloud.com',
    url="https://github.com/FredNoonienSingh/",
    packages=find_packages(exclude=["tests", "tests.*"]), #added exclude
    install_requires=['pandas', 'lxml', 'ollama'],  # external packages as dependencies
    setup_requires=['pytest-runner'], 
    tests_require=['pytest'],
    test_suite='tests',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)