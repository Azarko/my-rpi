# !/usr/bin/env python3

from os.path import isfile
from setuptools import find_packages, setup

if isfile('requirements.txt'):
    with open('requirements.txt') as stream:
        requirements = [line.strip() for line in stream.readlines()]
else:
    requirements = []


setup(
    version='1.0.0',
    name='my_rpi',
    packages=find_packages('.'),
    install_requires=requirements
)
