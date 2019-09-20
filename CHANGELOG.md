# Version History

## v1.0.0

- Add functionality to download .tar archives from NOAA
- Setup Travis-CI, Tox, CodeCov, ReadTheDocs, and PyUp to meet pyOpenSci publishing requirements for the future
- Download can be concurrent and stored on a cloud-based storage drive mounted locally
- Weakly ensures that when multiple people download files concurrently, the file they download is `locked` in a sense
- Add the basic functionality for a dashboard to tag images manually for future training / testing data