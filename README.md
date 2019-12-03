# Post-Storm Imagery Classification

[![Travis-CI](https://travis-ci.org/UNCG-CSE/Poststorm_Imagery.svg?branch=master)](
https://travis-ci.org/UNCG-CSE/Poststorm_Imagery)
[![CodeCov](https://codecov.io/gh/UNCG-CSE/Poststorm_Imagery/branch/master/graph/badge.svg?token=LWncqYANtK)](
https://codecov.io/gh/UNCG-CSE/Poststorm_Imagery/branch/master)
[![ReadTheDocs](https://readthedocs.org/projects/post-storm-imagery/badge/?version=master)](
https://post-storm-imagery.readthedocs.io/en/latest/?badge=master)

Classification and analysis of post-storm response imagery.

[![Documentation](https://img.shields.io/badge/Documentation-Click%20Me-brightgreen)](
https://post-storm-imagery.readthedocs.io/)

## Team Members

- [**Rinty Chowdhury**](https://github.com/rintychy)
- [**Daniel Foster**](https://github.com/dlfosterbot)
- [**Matthew Moretz**](https://github.com/Matmorcat)
- [**Shah Nafis Rafique**](https://github.com/ShahNafisRafique)
- [**John Weber**](https://github.com/JWeb56)

**Mentor:** [**Dr. Evan B. Goldstein**](https://github.com/ebgoldstein)

**Instructor:** [**Dr. Somya Mohanty**](https://github.com/somyamohanty)

## Contributions 🤝

### Code of Conduct

We hope to foster an inclusive and respectful environment surrounding the contribution and discussion of our project.
Make sure you understand our [**Code of Conduct**](https://post-storm-imagery.readthedocs.io/en/latest/code_of_conduct/).

### Code Conventions

Before committing to the repository **please** read the project
[**Code Conventions**](https://post-storm-imagery.readthedocs.io/en/latest/contributing/).

## Getting the Project Running 🏃‍

### Project Pre-Requisite

1. Python 3.6, 3.7, or 3.8 [**(Download Here)**](https://www.python.org/downloads/)

***You will need this in order to run the project.***

### Installing Dependencies

1. Change current directory (`cd`) to `Poststorm_Imagery/` (the project root)
2. Run `pipenv install` to install dependencies

### Collecting Data

1. Change current directory to the collector module (`cd collector/`)
2. Either use `pipenv run collect.py <args>` or `pipenv shell` then `collect.py <args>`

*The arguments for `collect.py` are listed [**here**](https://post-storm-imagery.readthedocs.io/en/latest/collector/)*


## Data Source 💾

- NOAA landing page for the post-storm imagery, [**here**]( https://storms.ngs.noaa.gov)
- USGS landing page, [**here**](https://coastal.er.usgs.gov/hurricanes/tools/oblique.php)
