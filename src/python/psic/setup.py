#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The setup script."""
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='psic',
    version='1.2.0',
    author='Team P-Sick',
    author_email='mcmoretz@uncg.edu',
    description='Classification and analysis of post-storm response imagery.',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
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
        'Programming Language :: Other',
        'Programming Language :: Other Scripting Engines',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/UNCG-CSE/Poststorm_Imagery',
    keywords='python',
    license='MIT license',
    install_requires=['jupyter', 'pandas', 'pillow', 'requests', 'tqdm'],
    include_package_data=True,
    packages=find_packages(),
    python_requires='>=3.6',
    test_suite='tests',
    tests_require=['bumpversion', 'flake8', 'pytest', 'pytest-cov', 'pytest-runner'],
    zip_safe=False,
)
