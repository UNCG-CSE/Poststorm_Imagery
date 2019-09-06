import os
import re
import tarfile

import requests
from tqdm import tqdm


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
        """Download a file from the given path. Whether or not to overwrite any existing file can also be specified by
        the `overwrite` variable
        Args:
            output_file_dir_path (str): The full or relative path (from src/collector/Tar.py) to download the file to
            overwrite (bool): Whether to overwrite the file or not. True = Overwrite any file with the same name, False
                = Don't overwrite file if a file by the same name exists.
        """

        # Add a separator to the end of the specified path if one doesn't exist
        if not output_file_dir_path.endswith('/') or not output_file_dir_path.endswith('\\'):

            # Ensure OS specific path separator is used (Windows = '\', Mac & Linux = '/')
            if re.search('(/)', output_file_dir_path):
                output_file_dir_path += '/'
            else:
                output_file_dir_path += '\\'

        # The full path of the file including the file name and file type
        self.tar_file_path = output_file_dir_path + str(self.tar_file_name) + '.tar'

        if not overwrite:

            # If the tar file does not exist locally in the cache
            if os.path.exists(output_file_dir_path) and os.path.isfile(self.tar_file_path):
                print('A file at ' + self.tar_file_path + ' already exists')
                return

        # Create the directory specified if it does not exist
        if not os.path.exists(output_file_dir_path):
            os.makedirs(output_file_dir_path)

        # Suffix for the file until download is complete
        tar_file_path_part: str = self.tar_file_path + '.part'

        # See how far a file has been downloaded at the specified path if one exists
        with open(tar_file_path_part, 'ab') as f:
            headers = {}
            pos = f.tell()
            if pos:
                # Add a header that specifies only to send back the bytes needed
                headers['Range'] = 'bytes=' + str(pos) + '-'

            # Send the HTTP request asking for the remaining bytes
            dl_r = requests.get(self.tar_url, headers=headers, stream=True)

            # Check if the server sent only the remaining data
            if dl_r.status_code == requests.codes.partial_content:
                print('Downloading the rest of ' + self.tar_file_name + '.tar ...')
            else:
                print('Downloading files...')

            # Get the amount of remaining bytes for the download
            total_size = int(dl_r.headers.get('content-length'))

            # Write the data and output the progress
            for data in tqdm(iterable=dl_r.iter_content(), desc='Progress (' + self.tar_file_name + '.tar)',
                             total=total_size, unit='B', unit_scale=True, miniters=1):
                f.write(data)

        # File download is complete. Change the name to reflect that it is a proper .tar file
        os.rename(tar_file_path_part, self.tar_file_path)

    def get_tar_info(self):
        """Loads an archive (.tar) into memory if it doesn't already exist"""

        if self.tar_index is None:

            # Open the tar file for reading with transparent compression
            self.tar_file = tarfile.open(self.tar_file_path, 'r')
            self.tar_index = self.tar_file.getmembers()

        return self.tar_index
