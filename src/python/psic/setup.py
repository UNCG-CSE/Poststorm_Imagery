#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The setup script."""
from setuptools import setup, find_packages

setup(
    name='psic',
    version='1.2.0',
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
<<<<<<< HEAD
    install_requires=['jupyter', 'pandas', 'pillow', 'requests', 'tqdm', 'imageio', 'imageio', 'matplotlib',
                      'tensorflow', 'scipy'],
=======
    install_requires=['requests', 'tqdm', 'jupyter', 'pandas', 'Pillow',
                      'jsonpickle', 'imageio', 'matplotlib'],
>>>>>>> 98eab92dcf338b14097ad7e96a9f9e822b56af47
    include_package_data=True,
    packages=find_packages(),
    test_suite='tests',
    tests_require=['bumpversion', 'flake8', 'pytest', 'pytest-cov', 'pytest-runner'],
    zip_safe=False,
)
