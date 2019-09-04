class Storm:

    storm_id: str
    storm_title: str
    storm_year: int

    def __init__(self, storm_id: str, storm_title: str, storm_year):
        self.storm_id = storm_id
        self.storm_title = storm_title
        self.storm_year = int(storm_year)

    def __str__(self):
        return self.storm_title + '(' + str(self.storm_year) + ')'
