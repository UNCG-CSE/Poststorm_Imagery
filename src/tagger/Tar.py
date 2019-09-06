import os
import re
import tarfile
import urllib.request

from tqdm import tqdm


class _ProgressBar(tqdm):
    """Provides `update_to(n)` which uses `tqdm.update(delta_n)` ."""

    def update_to(self, b=1, b_size=1, t_size=None):
        """Update a progress bar to show progress on a particular task

        Args:
            b (int): Number of blocks transferred so far [default: 1].
            b_size (int): Size of each block (in tqdm units) [default: 1].
            t_size (int): Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if t_size is not None:
            self.total = t_size
        self.update(b * b_size - self.n)


TAR_PATH_CACHE: str = '../../data/tar_cache/'

UNKNOWN = 'Unknown'


class Tar:
    """An object that stores information about a particular storm"""

    tar_date: str  # The date listed with the tar (format varies based on storm)
    tar_url: str  # The url location of the tar on the remote website
    tar_label: str  # The label associated with the tar (usually 'TIF', 'RAW JPEG', or 'Unknown')

    tar_file_name: str  # The .tar file's name not including the file suffix (.tar)
    tar_file_path: str  # The full path to the local copy of the .tar file, including file name and file suffix (.tar)

    tar_file: tarfile.TarFile  # The TarFile object stored in memory
    tar_index: tarfile.TarInfo = None  # The general info at the beginning of the TarFile object

    def __init__(self, tar_url: str, tar_date: str = UNKNOWN, tar_label: str = UNKNOWN):
        """Initializes the object with required information for a tar file

        Args:
            tar_url (str): The url to download the .tar file
            tar_date (str): The date that the archive corresponds to (format
                varies based on source URL)
            tar_label (str): The label associated with the archive
        """
        self.tar_date = tar_date
        self.tar_url = tar_url
        self.tar_label = tar_label

        # Grab the file name from the end of the URL
        self.tar_file_name = re.findall('.*/([^/]+)\\.tar', self.tar_url)[0]

    def __str__(self):
        """Prints out the tar label and date in a human readable format"""
        if self.tar_date == UNKNOWN and self.tar_label == UNKNOWN:
            return self.tar_file_name + '.tar'
        else:
            return '(' + self.tar_date + ') ' + self.tar_file_name + '.tar [' + self.tar_label + ']'

    def download_url(self, output_file_dir_path: str = TAR_PATH_CACHE, overwrite: bool = False):
        # TODO: Ensure user ends output file dir path with a / to prevent messed up file name
        """Download a file from the given path. Whether or not to overwrite any existing file can also be specified by
        the `overwrite` variable
        Args:
            output_file_dir_path (str): The full or relative path (from src/tagger/Tar.py) to download the file to
            overwrite (bool): Whether to overwrite the file or not. True = Overwrite any file with the same name, False
                = Don't overwrite file if a file by the same name exists.
        """
        self.tar_file_path = output_file_dir_path + str(self.tar_file_name) + '.tar'

        if not overwrite:

            # If the tar file does not exist locally in the cache
            if os.path.isfile(self.tar_file_path):
                print('A file at ' + self.tar_file_path + ' already exists')

            else:

                with _ProgressBar(unit='B', unit_scale=True, miniters=1,
                                  desc=self.tar_url.split('/')[-1]) as t:  # all optional kwargs
                    urllib.request.urlretrieve(self.tar_url, filename=self.tar_file_path,
                                               reporthook=t.update_to, data=None)

    def get_tar_info(self):
        """Loads an archive (.tar) into memory if it doesn't already exist"""

        if self.tar_index is None:

            # Open the tar file for reading with transparent compression
            self.tar_file = tarfile.open(self.tar_file_path, 'r')
            self.tar_index = self.tar_file.getmembers()

        return self.tar_index
