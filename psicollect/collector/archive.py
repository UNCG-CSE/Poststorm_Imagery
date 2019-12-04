import os
import re
import tarfile
import zipfile
from datetime import datetime, timedelta
from math import ceil
from tarfile import TarFile, TarInfo
from typing import Union
from zipfile import ZipFile, ZipInfo

import requests
from tqdm import tqdm

from psicollect.collector.locking import update_file_lock
from psicollect.collector.response_getter import get_full_content_length
from psicollect.common import h, s

UNKNOWN = 'Unknown'


class Archive:
    """An object that stores information about a particular storm. Does not store the actual archive archive by default,
    but instead stores a reference to the archive on a remote host (the NOAA website) and its information locally."""

    date: str  # The date listed with the archive (format varies based on storm)
    url: str  # The url location of the archive on the remote website
    type_label: str  # The label associated with the archive (usually 'TIF', 'RAW JPEG', or 'Unknown')

    name: str  # The archive file's name not including the file suffix
    type: str  # The archive file's type ('tar' or 'zip')

    # The full path to the local copy of the archive file, including file name and file suffix
    path: Union[bytes, str] or None = None

    data: TarFile or ZipFile  # The archive object stored in memory
    index: TarInfo or ZipInfo = None  # The general info at the beginning of the archive object

    # Save a cache of the file size in bytes
    file_origin_size: int or None = None

    def __init__(self, archive_url: str, archive_date: str = UNKNOWN, archive_label: str = UNKNOWN):
        """Initializes the object with required information for a archive file

        :param archive_url: The url to download the archive file
        :param archive_date: The date that the archive corresponds to (format varies based on source URL)
        :param archive_label: The label associated with the archive
        """
        self.date = archive_date
        self.url = archive_url
        self.type_label = archive_label

        # Parse out needed information from the URL
        self.name, self.type = re.findall(re.compile('.*/([^/]+)\\.(tar|zip)', re.IGNORECASE), self.url)[0]

        # Make sure the type is lower-case (e.g. don't distinguish between 'ZIP' and 'zip')
        self.type = self.type.lower()

    def __str__(self) -> str:
        """Prints out the archive label and date in a human readable format"""
        if self.date == UNKNOWN and self.type_label == UNKNOWN:
            return self.name + self.get_ext()
        else:
            return '(' + self.date + ') ' + self.name + self.get_ext() + ' [' + self.type_label + ']'

    def get_ext(self) -> str:
        """Simply get the file extension for this archive (e.g. '.tar' or '.zip')

        :returns: The file extension (e.g. '.tar' or '.zip') as a string
        """
        return '.' + self.type

    def is_zip(self) -> bool:
        """Simply get if the archive is a .zip archive

        :returns: Whether (True) or not (False) the archive is a .zip archive
        """
        return self.type == 'zip'

    def is_tar(self) -> bool:
        """Simply get if the archive is a .tar archive

        :returns: Whether (True) or not (False) the archive is a .tar archive
        """
        return self.type == 'tar'

    def download_url(self, output_dir: str, user: str, overwrite: bool = False) \
            -> Union[TarFile, ZipFile, None]:  # pragma: no cover
        """Download the archive file to the given path. Whether or not to overwrite
        any existing file can also be specified by the `overwrite` parameter.

        :param user: The user to download as (locking mechanism)
        :param output_dir: The location to save the downloaded archive file to (a path on the local machine)
        :param overwrite: Whether or not to overwrite a file if one already exists by the same name
        :returns: The archive file that was downloaded
        """
        # The full path of the file including the file name and file type
        self.path = os.path.join(output_dir, str(self.name) + self.get_ext())

        if not overwrite:

            # If the archive file does not exist locally in the cache
            if os.path.exists(output_dir) and os.path.isfile(self.path):
                print('File \"' + self.path + '\" already exists!  ... Skipping')
                if self.is_tar():
                    return tarfile.open(self.path)
                else:
                    return ZipFile(self.path)

        # Create the directory specified if it does not exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Suffix for the file until download is complete
        file_path_part: str = self.path + s.PART_SUFFIX

        # See how far a file has been downloaded at the specified path if one exists
        with open(file_path_part, 'ab') as f:
            headers = {}
            pos = f.tell()

            full_size_origin = self.get_file_size_origin()

            if pos:
                # Add a header that specifies only to send back the bytes needed
                headers['Range'] = 'bytes=' + str(pos) + '-' + str(full_size_origin)

            # Send the HTTP request asking for the remaining bytes
            dl_r = requests.get(self.url, headers=headers, stream=True)

            # Check if the server sent only the remaining data
            if dl_r.status_code == requests.codes.partial_content:
                print('\nDownloading the rest of ' + self.name + self.get_ext() + ' ...')
            else:
                print('\nDownloading files...')

            # Get the current amount of bytes downloaded
            local_size = os.path.getsize(file_path_part)

            # Get the amount of remaining bytes for the download
            remaining_size = int(dl_r.headers.get('Content-Length'))

            full_size_local: int = local_size + remaining_size

            # Ensure that both the program and the website are on the same page
            if full_size_local != full_size_origin:
                h.print_error('Remaining file size does not match with local cache. '
                              'Something went wrong with partial file request!')
                exit(1)

            # How many bytes to load into memory before saving to the file
            chunk_size: int = 1024 * 1024

            # The label of the given chunk size above (1024 * 1024 Bytes = 1 MiB)
            unit = 'MiB'

            last_lock_update = datetime.now() - timedelta(hours=1)

            # Write the data and output the progress
            for data in tqdm(iterable=dl_r.iter_content(chunk_size=chunk_size),
                             desc='Downloading ' + self.name + self.get_ext(),
                             total=ceil((remaining_size + local_size) / chunk_size),
                             initial=ceil(local_size / chunk_size), unit=unit, miniters=1):

                # Update the lock file every so often so others know it is being downloaded
                if (datetime.now() - last_lock_update).total_seconds() > 180:  # 1800 seconds = 30 minutes
                    update_file_lock(base_file=file_path_part, user=user,
                                     part_size_byte=os.path.getsize(file_path_part),
                                     total_size_byte=full_size_origin)
                f.write(data)

            dl_r.close()

        local_size = os.path.getsize(file_path_part)

        # Check to see that the file size is correct (in case of dropped connection)
        if local_size < full_size_origin:
            raise ConnectionError('File was not fully downloaded. Retry download!')

        # File download is complete. Change the name to reflect that it is a proper archive file
        os.rename(file_path_part, self.path)

        # Remove the lock file
        os.remove(file_path_part + s.LOCK_SUFFIX)

        # Tell others that the full file is downloaded
        update_file_lock(base_file=self.path, user=user,
                         total_size_byte=full_size_origin, part_size_byte=full_size_origin)

        if Archive.verify_integrity(self.path) is False:
            os.remove(self.path)
            Exception('Integrity could not be verified! Deleting it!')

        else:
            print('Extracting files...')
            Archive.extract_archive(self.path)

        if self.is_tar():
            return tarfile.open(self.path)
        else:
            return ZipFile(self.path)

    def get_file_size_origin(self) -> int:  # pragma: no cover
        """Checks to see if the Archive object has its full size cached. If it doesn't then it will make a request to
        the website and get the size of the archive file from the header.

        :return: The size of the archive file in bytes
        """
        if self.file_origin_size is not None:
            return self.file_origin_size

        return get_full_content_length(self.url)

    @staticmethod
    def verify_integrity(archive_file_path: Union[bytes, str]) -> bool:
        """Takes in a file's path and reads through each record in the archive's index to see if it is valid. This does
        not ensure that the file is completely error-free, but ensures that the archive has some validity.

        :param archive_file_path: The path to the file to check
        :return: True if the file seems valid, False if it does not
        """
        print('Checking the archive\'s integrity...')
        # Check archive integrity by trying to read every file (may take a while)
        try:
            if tarfile.is_tarfile(archive_file_path):
                with tarfile.open(archive_file_path) as f:

                    # Test the tar archive for some possible errors by trying to load each image from the archive
                    for member in f.getmembers():
                        # print('    Testing member ' + member.name + '...')
                        f.extractfile(member.name)

            elif zipfile.is_zipfile(archive_file_path):
                with zipfile.ZipFile(archive_file_path) as f:

                    # Built in method checks CRCs and returns first file w/ error (returns None if all is good)
                    first_error = f.testzip()

                    if first_error is not None:  # pragma: no cover
                        # A file is corrupted

                        raise IOError('File %s was found to be corrupted in the archive!' % first_error)

            else:  # pragma: no cover
                raise IOError('File is not of a supported archive type!')

        except IOError as e:  # pragma: no cover
            h.print_error('There was an error in reading ' + archive_file_path + ' file. It might be corrupted!')
            h.print_error('It is recommended to delete the archive and restart the download.')
            h.print_error('Error: ' + str(e))

            return False

        return True

    @staticmethod
    def extract_archive(archive_file_path: Union[bytes, str]):
        """Extract all the contents of a archive file into a directory of the same name (minus the file extension).

        :param archive_file_path: The path to the archive file (including the file extension) to extract
        """

        f: TarFile or ZipFile
        f_members: list

        if tarfile.is_tarfile(archive_file_path):
            f = tarfile.open(archive_file_path)
            f_members = f.getmembers()
        elif zipfile.is_zipfile(archive_file_path):
            f = zipfile.ZipFile(archive_file_path)
            f_members = f.infolist()
        else:  # pragma: no cover
            raise IOError('File is not of a supported archive type!')

        # Extract to a directory of the same name, but without the file extension
        extract_dir_path = os.path.splitext(archive_file_path)[0]

        # Create the directory specified if it does not exist
        if not os.path.exists(extract_dir_path):
            os.makedirs(extract_dir_path)

        for member in f_members:

            name: str  # The name of the member
            if type(member) == ZipInfo:
                name = member.filename
            else:
                name = member.name

            if os.path.exists(os.path.join(extract_dir_path, os.path.split(name)[1])) is False:
                print('\rCreating \t' + name + ' ... ', end='')
                f.extract(member, extract_dir_path)
            elif member.name != '.':
                print('\rSkipping \t' + name + ' as it already exists ... ', end='')

        f.close()
