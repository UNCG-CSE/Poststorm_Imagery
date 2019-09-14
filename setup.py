#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
setup_requirements = ['pytest-runner', 'pipenv']
from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip
from setuptools import setup

# with open('README.md') as readme_file:
#     readme = readme_file.read()

pipfile = Project(chdir=False).parsed_pipfile
requirements = convert_deps_to_pip(pipfile['packages'], r=False)
test_requirements = convert_deps_to_pip(pipfile['dev-packages'], r=False)

setup(
    author="Matthew Charles Moretz",
    author_email='mcmoretz@uncg.edu',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Classification and analysis of post-storm response imagery.",
    install_requires=requirements,
    license="MIT license",
    # long_description=readme,
    include_package_data=True,
    keywords='python',
    name='python',
    # packages=find_packages(include=['python']),
    packages=['src/python/Poststorm_Imagery'],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/UNCG-CSE/Poststorm_Imagery',
    version='0.5.4',
    zip_safe=False,
)
