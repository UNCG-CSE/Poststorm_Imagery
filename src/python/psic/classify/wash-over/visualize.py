import random
from getpass import getuser
from os import path

import cv2
import numpy as np
import pandas as pd

random.seed = 405

if getuser() == 'mattm':
    DRIVE_PATH = 'F:\\Shared drives\\P-Sick'
else:
    DRIVE_PATH = 'mnt/Secondary/mcmoretz@uncg.edu/C-Sick'

FINAL_TAGS_CSV = path.join(DRIVE_PATH, 'tag_csv/tagging_data.csv')
SMALL_IMAGES_DIR = path.join(DRIVE_PATH, 'small/Florence/20180917a_jpgs/jpgs')

data = pd.read_csv(FINAL_TAGS_CSV, usecols=['image_id', 'washover'])

data['image'] = np.NaN
print(data)

for i, row in data.iterrows():
    print(row.keys())
    image_path = path.join(SMALL_IMAGES_DIR, row['image_id'])

    # Load grayscale versions of the small images
    image = cv2.imread(image_path, 0)
    row['image'] = image

data.drop(columns=['image_id'], inplace=True)
print(data)
