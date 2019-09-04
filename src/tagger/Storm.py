import tarfile
from typing import List


class Storm:

    storm_id: str
    storm_title: str
    storm_year: int

    tar_file: tarfile.TarFile
    tar_index: List[tarfile.TarInfo]

    def __init__(self, storm_id: str, storm_title: str, storm_year):
        self.storm_id = storm_id
        self.storm_title = storm_title
        self.storm_year = int(storm_year)

    def __str__(self):
        return self.storm_title + '(' + str(self.storm_year) + ')'

    def load_data(self, tar_url: str):
        """

        Load an archive (.tar) into memory
        :param tar_url: str
        """
        # Open the tar file for reading with transparent compression
        self.tar_file = tarfile.open(tar_url, 'r')
        self.tar_index = self.tar_file.getmembers()
