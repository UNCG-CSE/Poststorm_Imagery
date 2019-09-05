import tarfile
from typing import List


class Storm:
    """An object that stores information about a particular storm"""

    storm_url: str
    storm_id: str
    storm_title: str
    storm_year: int

    tar_file: tarfile.TarFile
    tar_index: List[tarfile.TarInfo]

    def __init__(self, storm_url: str, storm_id: str, storm_title: str, storm_year: str or int):
        """Initializes the object with required information for a storm

        Args:
            storm_id (str): The ID (from URL) of the storm
            storm_title (str): The name (link name) of the storm
            storm_year (str or int): The year the storm occurred
        """
        self.storm_url = storm_url
        self.storm_id = storm_id
        self.storm_title = storm_title
        self.storm_year = int(storm_year)

    def __str__(self):
        """Prints out the storm title and year in a human readable format"""
        return self.storm_title + '(' + str(self.storm_year) + ')'

    def load_data(self, tar_url: str):
        """Loads an archive (.tar) into memory

        Args:
            tar_url (str): The link to the .tar file to open
        """
        # Open the tar file for reading with transparent compression
        self.tar_file = tarfile.open(tar_url, 'r')
        self.tar_index = self.tar_file.getmembers()
