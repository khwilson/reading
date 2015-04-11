import os
from setuptools import setup, find_packages
from setuptools.command.install import install
import sys


def parse_requirements(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name), 'r') as f:
        return [l.strip() for l in f if not l.startswith('#') and l.strip()]


setup(
    name='reading',
    version='0.0.1',
    url='https://github.com/khwilson/reading',
    author='Kevin Wilson',
    author_email='khwilson@gmail.com',
    license='BSD',
    packages=find_packages(),
    scripts=['bin/reading'],
    include_package_data=True,
    zip_safe=False,
    install_requires=parse_requirements('requirements.txt'),
    description='A simple web application to send books and messages to kids.',
    long_description=open('README.rst').read()
)
