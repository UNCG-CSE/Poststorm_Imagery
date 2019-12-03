#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The setup script."""
from setuptools import setup, find_packages


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='psicollect',
    version='1.4.0',
    author='Team P-Sick',
    author_email='mcmoretz@uncg.edu',
    url='https://github.com/UNCG-CSE/Poststorm_Imagery',
    description='Collection, aggregation, and cataloging of storm imagery for '
                'the purpose of data sciences and analysis.',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Framework :: Flake8',
        'Framework :: Pytest',
        'Framework :: tox',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
    ],
    keywords='python',
    license='MIT license',
    install_requires=required,
    packages=find_packages(),
    python_requires=">=3.6",
    zip_safe=False,
)
