import os
import re
import tarfile
from math import ceil
from typing import Union

import requests
from tqdm import tqdm

UNKNOWN = 'Unknown'


class TarRef:
    """An object that stores information about a particular storm"""

    tar_date: str  # The date listed with the tar (format varies based on storm)
    tar_url: str  # The url location of the tar on the remote website
    tar_label: str  # The label associated with the tar (usually 'TIF', 'RAW JPEG', or 'Unknown')

    tar_file_name: str  # The .tar file's name not including the file suffix (.tar)
    tar_file_path: Union[bytes, str]  # The full path to the local copy of the .tar file, including file name and file suffix (.tar)

    tar_file: tarfile.TarFile  # The TarFile object stored in memory
    tar_index: tarfile.TarInfo = None  # The general info at the beginning of the TarFile object

    def __init__(self, tar_url: str, tar_date: str = UNKNOWN, tar_label: str = UNKNOWN):
        """Initializes the object with required information for a tar file

        :param tar_url: The url to download the .tar file
        :param tar_date: The date that the archive corresponds to (format varies based on source URL)
        :param tar_label: The label associated with the archive
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

    def download_url(self, output_dir: str, overwrite: bool = False) -> tarfile.TarFile:
        """Download the tar file to the given path. Whether or not to overwrite
        any existing file can also be specified by the `overwrite` variable.

        :param output_dir: The location to save the downloaded tar file to (a path on the local machine)
        :param overwrite: Whether or not to overwrite a file if one already exists by the same name
        :returns: The tar file that was downloaded
        """
        # The full path of the file including the file name and file type
        self.tar_file_path = os.path.join(output_dir, str(self.tar_file_name) + '.tar')

        if not overwrite:

            # If the tar file does not exist locally in the cache
            if os.path.exists(output_dir) and os.path.isfile(self.tar_file_path):
                print('File \"' + self.tar_file_path + '\" already exists. (Specify flag \'-o\' to overwrite)')
                return tarfile.open(self.tar_file_path)

        # Create the directory specified if it does not exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Suffix for the file until download is complete
        tar_file_path_part: str = self.tar_file_path + '.part'

        # See how far a file has been downloaded at the specified path if one exists
        with open(tar_file_path_part, 'ab') as f:
            headers = {}
            pos = f.tell()

            # Ask the server for head
            dl_r_full = requests.head(self.tar_url, stream=True)

            # Ask the server how big its' package is
            full_size_origin = int(dl_r_full.headers.get('Content-Length'))

            # Stop talking to the server about this
            dl_r_full.close()

            if pos:
                # Add a header that specifies only to send back the bytes needed
                headers['Range'] = 'bytes=' + str(pos) + '-' + str(full_size_origin)

            # Send the HTTP request asking for the remaining bytes
            dl_r = requests.get(self.tar_url, headers=headers, stream=True)

            # Check if the server sent only the remaining data
            if dl_r.status_code == requests.codes.partial_content:
                print('Downloading the rest of ' + self.tar_file_name + '.tar ...')
            else:
                print('Downloading files...')

            # Get the current amount of bytes downloaded
            local_size = os.path.getsize(tar_file_path_part)

            # Get the amount of remaining bytes for the download
            remaining_size = int(dl_r.headers.get('Content-Length'))

            full_size_local: int = local_size + remaining_size

            # Ensure that both the program and the website are on the same page
            if full_size_local != full_size_origin:
                print('Remaining file size does not match with local cache. '
                      'Something went wrong with partial file request!')
                exit()

            # How many bytes to load into memory before saving to the file
            chunk_size: int = 1024 * 1024

            # The label of the given chunk size above (1024 * 1024 Bytes = 1 MiB)
            unit = 'MiB'

            # Write the data and output the progress
            for data in tqdm(iterable=dl_r.iter_content(chunk_size=chunk_size), desc='Downloading ' + self.tar_file_name + '.tar',
                             total=ceil((remaining_size + local_size) / chunk_size),
                             initial=ceil(local_size / chunk_size), unit=unit, miniters=1):
                f.write(data)

            dl_r.close()

            local_size = os.path.getsize(tar_file_path_part)

            # Check to see that the file size is correct (in case of dropped connection)
            if full_size_local != full_size_origin:
                raise ConnectionError('File was not fully downloaded. Retry download!')

        # File download is complete. Change the name to reflect that it is a proper .tar file
        os.rename(tar_file_path_part, self.tar_file_path)

        return tarfile.open(self.tar_file_path)