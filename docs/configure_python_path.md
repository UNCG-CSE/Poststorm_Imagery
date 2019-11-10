# Configuring Python Path

## Requirements
This guide assumes you obtained a copy of this project by cloning it from
[our repository](https://github.com/UNCG-CSE/Poststorm_Imagery/).

## Actions

Let your python interpreter know where to look in order to find the `psic` module.
The `psic` module is located under `src/python` in the project, so we'll need to `export` the `src/python` folder as
`PYTHONPATH`.

### Linux

1.  Add the line `export PYTHONPATH="<path to project>/src/python"` to
    the end of the file `~/.bashrc` using your favorite text editor
    (e.g. `nano ~/.bashrc` for the *nano* text editor).
    This will ensure that your python interpreter knows where to look.

2. Log-out and log back in to trigger the `~/.bashrc` file.

### Windows 10

1.  Click `Start` in the bottom-left
2.  Search `environment variables`
3.  Click `Edit the system environment variables` in the search results
4.  Click the `Environment Variables...` button in the bottom right-hand corner of the window that pops up
5.  Click `New...` and add the variable as either a user or system variable.
    Variable name will be `PYTHONPATH` and value will be `<path to project>/src/python`


!!! error "Module not found: 'psic'"
    If you get an error that says something like `Module 'psic' not found!`, then the python interpreter can't
    find the project. Double-check that the project is in the `PYTHONPATH`. You should see it in your environment
    variables when running `env` from terminal in **Linux** or in the environmental variables screen in **Windows 10**.
