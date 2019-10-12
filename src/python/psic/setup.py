#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
"""
from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip

pip_file = Project().parsed_pipfile
requirements = convert_deps_to_pip(pip_file['packages'], r=False)
test_requirements = convert_deps_to_pip(pip_file['dev-packages'], r=False)
"""

setup(
    name='psic',
    version='1.1.0',
    author='Team P-Sick',
    author_email='mcmoretz@uncg.edu',
    url='https://github.com/UNCG-CSE/Poststorm_Imagery',
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
    keywords='python',
    license='MIT license',
    install_requires='requirements.txt',
    include_package_data=True,
    packages=find_packages(),
    test_suite='tests',
    tests_require='requirements-dev.txt',
    zip_safe=False,
)
