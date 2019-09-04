class Storm:

    storm_id: str
    storm_title: str
    storm_year: str

    def __init__(self, storm_id: str, storm_title: str, storm_year):
        self.storm_id = storm_id
        self.storm_title = storm_title
        self.storm_year = storm_year

    def __str__(self):
        return self.storm_title + '(' + self.storm_year + ')'
