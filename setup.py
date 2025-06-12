# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 11:10:39 2025

@author: du
"""

from setuptools import setup, find_packages

setup(
    name='meshcode_pkg',
    version='0.1',
    packages=find_packages(),
    install_requires=['shapely'],
    description='Convert lat/lon to Japanese meshcode and vice versa',
    author='Ran DU',
    author_email='durianranger94@gmail.com',
    license='MIT',
    zip_safe=False,
)
