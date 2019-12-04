#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The setup script."""
from setuptools import setup, find_packages

REPO_URL = 'https://github.com/UNCG-CSE/Poststorm_Imagery'
DOCS_URL = 'https://post-storm-imagery.readthedocs.io/en/latest/'

with open('README.md', 'r', encoding='utf8') as fh:
    long_description = fh.read()

setup(
    name='psi-collect',
    version='0.3.1',
    author='Team P-Sick',
    author_email='mcmoretz@uncg.edu',
    description='Collection, aggregation, and cataloging of storm imagery for '
                'the purpose of data sciences and analysis.',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
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
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['requests', 'tqdm', 'pandas', 'Pillow', 'imageio'],
    package_data={'catalogs': ['data/catalogs']},
    packages=find_packages(include=['psicollect.*']),
    project_urls={
        'Documentation': DOCS_URL,
        'Source': REPO_URL,
        'Tracker': REPO_URL + '/issues',
    },
    python_requires='>=3.6',
    entry_points={  # Executable scripts as command-line
        'console_scripts': [
            'pstorm=psicollect.common.pstorm:main',
        ],
    },
    url=REPO_URL,
    zip_safe=False,
)
