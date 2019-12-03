# Contribution Conventions

When committing to the repository, there are a few conventions that should be followed.

## Code Style

- Code is clean and commented where needed
- Any unused code is either removed or commented out
- Methods that are not entirely obvious as to how they work should have a doc comment explaining the purpose and
  arguments (see [Storm.py](https://github.com/UNCG-CSE/Poststorm_Imagery/blob/master/psicollect/collector/storm.py)
  for an example)
- Code with different functions should be reasonably separated by directories of their function
- When changing any functions, documentation referencing that code should be changed to match (.md files / doc comments)
- If changes are made to another person's code that fundamentally change the output / input of the code, discuss those
changes with the original creator

## Handling Branches

| Branch | Purpose                                                           |
| ------ | ----------------------------------------------------------------- |
| Master | Bug fixes & general addition                                      |
| Others | New distinct features that are incomplete / not functional yet    |

## Project & External Data

- All large data files must be excluded from the GitHub repository.
  *Note: All files except `.gitignore` files are ignored in the `data` folder, so storing data in a sub-directory
  there is a good option! To force Git to commit a directory, but not the files in it, you can copy
  the `.gitignore` from `data/archive_cache` into the directory.*
