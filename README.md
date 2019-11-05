# Post-Storm Imagery Classification

[![Travis-CI](https://travis-ci.org/UNCG-CSE/Poststorm_Imagery.svg?branch=master)](
https://travis-ci.org/UNCG-CSE/Poststorm_Imagery)
[![CodeCov](https://codecov.io/gh/UNCG-CSE/Poststorm_Imagery/branch/master/graph/badge.svg?token=LWncqYANtK)](
https://codecov.io/gh/UNCG-CSE/Poststorm_Imagery/branch/master)
[![ReadTheDocs](https://readthedocs.org/projects/post-storm-imagery/badge/?version=master)](
https://post-storm-imagery.readthedocs.io/en/latest/?badge=master)
[![PyUp](https://pyup.io/repos/github/UNCG-CSE/Poststorm_Imagery/shield.svg?branch=master)](
https://pyup.io/repos/github/UNCG-CSE/Poststorm_Imagery/)

Classification and analysis of post-storm response imagery.

[![Documentation](https://img.shields.io/badge/Documentation-Click%20Me-brightgreen)](
https://post-storm-imagery.readthedocs.io/)

## Team Members

- [**Rinty Chowdhury**](https://github.com/rintychy)
- [**Daniel Foster**](https://github.com/dlfosterbot)
- [**Matthew Moretz**](https://github.com/Matmorcat)
- [**Shah Nafis Rafique**](https://github.com/ShahNafisRafique)
- [**John Weber**](https://github.com/JWeb56)

**Instructor:** [**Dr. Somya Mohanty**](https://github.com/somyamohanty)
**Mentor:** [**Dr. Evan B. Goldstein**](https://github.com/ebgoldstein)

## Contributions 🤝

### Code of Conduct

We hope to foster an inclusive and respectful environment surrounding the contribution and discussion of our project.
Make sure you understand our [**Code of Conduct**](https://post-storm-imagery.readthedocs.io/en/latest/code_of_conduct/).

### Code Conventions

Before committing to the repository **please** read the project
[**Code Conventions**](https://post-storm-imagery.readthedocs.io/en/latest/contributing/).

### Beta Branch

[![Travis-CI](https://travis-ci.org/UNCG-CSE/Poststorm_Imagery.svg?branch=beta)](
https://travis-ci.org/UNCG-CSE/Poststorm_Imagery)
[![CodeCov](https://codecov.io/gh/UNCG-CSE/Poststorm_Imagery/branch/beta/graph/badge.svg?token=LWncqYANtK)](
https://codecov.io/gh/UNCG-CSE/Poststorm_Imagery/branch/beta)
[![ReadTheDocs](https://readthedocs.org/projects/post-storm-imagery/badge/?version=beta)](
https://post-storm-imagery.readthedocs.io/en/latest/?badge=beta)
[![PyUp](https://pyup.io/repos/github/UNCG-CSE/Poststorm_Imagery/shield.svg?branch=beta)](
https://pyup.io/repos/github/UNCG-CSE/Poststorm_Imagery/)

Beta branch is the main place to submit new code.

## Getting the Project Running 🏃‍

### Project Pre-Requisites

1. Python 3.6 or 3.7 [**(Download Here)**](https://www.python.org/downloads/)
2. Pipenv **(Run `pip install pipenv`)**
3. You will need to add the folder containing the `psic` module (`src/python` by default) to your `PYTHONPATH`.

*If you get an error message that looks something like `Module not found: "psic"`,
then the `PYTHONPATH` is not configured correctly!*

***You will need these in order to run the project.***

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
