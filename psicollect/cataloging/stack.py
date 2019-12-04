#!/usr/bin/env python3
from os import listdir
from os.path import isfile, join, splitext

import pandas as pd

from psicollect.common import s

# Get all storm-specific CSV files in the catalogs folder (e.g. data/catalogs/v2)
catalogs = [f for f in listdir(s.CATALOG_DATA_PATH) if isfile(join(s.CATALOG_DATA_PATH, f))
            and str(splitext(join(s.CATALOG_DATA_PATH, f))[1]) == '.csv'
            and str(f) != s.CATALOG_FILE_GLOBAL]

catalogs_str: str = ''
for catalog in catalogs:

    if len(catalogs_str) != 0:
        # Before everything, but the first catalog
        catalogs_str += ', '

    if catalog == catalogs[-1]:
        # Before the last catalog
        catalogs_str += 'and '

    catalogs_str += str(splitext(catalog)[0])

print('Found catalogs (%d): %s.' % (len(catalogs), catalogs_str))

combined: pd.DataFrame or None = None

for catalog in catalogs:

    # Open the catalog file and read in the data to a DataFrame
    # Makes sure to drop the first column (index / id of individual catalog entries)
    curr_data: pd.DataFrame = pd.read_csv(join(s.CATALOG_DATA_PATH, catalog), header=0).drop('Unnamed: 0', axis=1)

    if combined is None:
        # If the combined catalog is currently empty, just fill it with the first catalog's data
        combined = curr_data
    else:
        # Data already exists in the combined catalog
        combined = combined.append(curr_data, sort=False, ignore_index=True)

if s.DEFAULT_DEBUG:
    print(combined)

# Save the combined catalog to the disk
combined.to_csv(join(s.CATALOG_DATA_PATH, s.CATALOG_FILE_GLOBAL))
print('Saved complete catalog to disk!')
