# Post-Storm Imagery Collection

[![Travis-CI](https://travis-ci.org/UNCG-CSE/Poststorm_Imagery.svg?branch=master)](
https://travis-ci.org/UNCG-CSE/Poststorm_Imagery)
[![CodeCov](https://codecov.io/gh/UNCG-CSE/Poststorm_Imagery/branch/master/graph/badge.svg?token=LWncqYANtK)](
https://codecov.io/gh/UNCG-CSE/Poststorm_Imagery/branch/master)
[![ReadTheDocs](https://readthedocs.org/projects/post-storm-imagery/badge/?version=master)](
https://post-storm-imagery.readthedocs.io/en/latest/?badge=master)

Collection, aggregation, and cataloging of storm imagery for the purpose of data sciences and analysis.

[![Documentation](https://img.shields.io/badge/Documentation-Click%20Me-brightgreen)](
https://post-storm-imagery.readthedocs.io/)

## Team Members

- [**Matthew Moretz**](https://github.com/Matmorcat)
- [**Daniel Foster**](https://github.com/dlfosterbot)
- [**Evan Goldstein**](https://github.com/ebgoldstein)
- [**Somya Mohanty**](https://github.com/somyamohanty)
- [**John Weber**](https://github.com/JWeb56)
- [**Rinty Chowdhury**](https://github.com/rintychy)
- [**Shah Nafis Rafique**](https://github.com/ShahNafisRafique)

## Usage

1. Install Python 3.6, 3.7, or 3.8 [**(Download Here)**](https://www.python.org/downloads/)
2. Run `pip3 install psi-collect` in your favorite terminal
3. Run `pstorm collect -h` for help on collecting images or `pstorm catalog -h` for help on cataloging local archives

## Contributing / Developing

### Code of Conduct

We hope to foster an inclusive and respectful environment surrounding the contribution and discussion of our project.
Make sure you understand our [**Code of Conduct**](https://post-storm-imagery.readthedocs.io/en/latest/code_of_conduct/).

### Code Conventions

Before committing to the repository **please** read the project
[**Code Conventions**](https://post-storm-imagery.readthedocs.io/en/latest/contributing/).

### Project Pre-Requisites

1. Python 3.6, 3.7, or 3.8 [**(Download Here)**](https://www.python.org/downloads/)
2. Pipenv **(Run `pip install pipenv`)**
3. You will need to add the folder containing the `psic` module (`src/python` by default) to your `PYTHONPATH`
   (See [**Configuring Module**](https://post-storm-imagery.readthedocs.io/en/latest/configure_python_path/))

*If you get an error message that looks something like `Module not found: "psic"`,
then the `PYTHONPATH` is not configured correctly!*

***You will need this in order to run the project.***

### Installing Dependencies for Development

1. Change current directory (`cd`) to `Poststorm_Imagery/` (the project root)
2. Run `pipenv install` to install dependencies

### Testing the Collect Script

1. Change current directory to the collector module (`cd collector/`)
2. Either use `pipenv run collect.py <args>` or `pipenv shell` then `collect.py <args>`

*The arguments for `collect.py` are listed [**here**](https://post-storm-imagery.readthedocs.io/en/latest/collector/)*


## Data Source 💾

- NOAA landing page for the post-storm imagery, [**here**]( https://storms.ngs.noaa.gov)
- USGS landing page, [**here**](https://coastal.er.usgs.gov/hurricanes/tools/oblique.php)
