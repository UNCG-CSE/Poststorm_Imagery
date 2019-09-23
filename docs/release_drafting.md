# Drafting New Releases


## Updating Version Fields in Source

Before drafting a release, you want to make sure that all of the version fields for the project including those found
python's `__init__.py`, MkDoc's version flag, and more are updated with the new version.

This can be done by command-line:

1.  Setup the project by following the instructions found [**here**](./index.md)

2.  Navigate to the python root directory (`cd src/python`) if not already there

3.  Run `pipenv shell` to open a shell for the virtual environment

4.  Install the BumpVersion plugin (`pip install bumpversion`)

5.  Once installed run `bumpversion <change_type>`

This will update the version number like so...

| Change Type | Examples (Before -> After)     |
| ----------- | ------------------------------ |
| Major       | v1.0.0 -> v2.0.0               |
|             | v1.3.5 -> v2.0.0               |
| Minor       | v1.0.0 -> v1.1.0               |
|             | v1.3.5 -> v1.4.0               |
| Patch       | v1.0.0 -> v1.0.1               |
|             | v1.3.5 -> v1.3.6               |

| Change Type | Description                                                                                           |
| ----------- | ----------------------------------------------------------------------------------------------------- |
| Major       | Will significantly change previous releases' code where the user must manually make changes to update |
| Minor       | Changes that won't break previous releases, but add significant new content                           |
| Patch       | Fixes and improvements for existing code with very little new functionality added                     |

*Example:* If I add a new system for tagging images that has a lot of new code for a new part of a project for 
example, I would run `bumpversion minor`. This will update the minor version (The second decimal-separated number 
of the version number)

The nitty-gritty of this versioning scheme can be found in the 
[**Semantic Versioning Specifications**](https://semver.org/)

## Documenting the Release

1.  Finally, update the `CHANGELOG.md` with the new version and all the major changes that have been done since the 
    last release. Small tweaks are not necessary, it's mainly just the big changes the user will notice!
    
2.  Commit and push all changes to `origin/beta`, then pull the changes into `origin/master` and select 
    `draft new release`. 
    
3.  Paste the latest entry from the `CHANGELOG.md` if it is not auto-filled and add the tag for 
    the version as it is in the source and `CHANGELOG.md`.
    
4.  Get someone to review it for errors as this is a public snapshot of progress.

5. Publish the release with an appropriate title after it has been reviewed.
    
    