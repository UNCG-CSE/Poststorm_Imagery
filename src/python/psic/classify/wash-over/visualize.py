import random
from os import path

import cv2
import numpy as np
import pandas as pd

random.seed = 405

data = pd.read_csv('/mnt/Secondary/mcmoretz@uncg.edu/C-Sick/tag_csv/tagging_data.csv', usecols=['image_id', 'washover'])

data['image'] = np.NaN
print(data)

for i, row in data.iterrows():
    print(row.keys())
    image_path = path.join('/mnt/Secondary/mcmoretz@uncg.edu/C-Sick/small/Florence/20180917a_jpgs/jpgs',
                           row['image_id'])

    # Load grayscale versions of the small images
    image = cv2.imread(image_path, 0)
    row['image'] = cv2.imread(image_path, 0)
    image.close()

data.drop(columns=['image_id'], inplace=True)
print(data)
