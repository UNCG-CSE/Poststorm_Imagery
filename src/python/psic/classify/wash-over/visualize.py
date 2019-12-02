import random
from getpass import getuser
from os import path

import cv2
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.model_selection import train_test_split

from psic.resizer.generate import ResizeImages

SEED = 405

random.seed = SEED

if getuser() == 'mattm':
    DRIVE_PATH = 'F:\\Shared drives\\P-Sick'
else:
    DRIVE_PATH = 'mnt/Secondary/mcmoretz@uncg.edu/C-Sick'

FINAL_TAGS_CSV = path.join(DRIVE_PATH, 'tag_csv/tagging_data.csv')
SMALL_IMAGES_DIR = path.join(DRIVE_PATH, 'vsmall/5/Florence/20180917a_jpgs/jpgs')

# Create new compressed images that are 5% of original image sizes using nearest neighbor selection
ResizeImages.resize_all_images(path=path.join(DRIVE_PATH, 'data/Florence/20180917a_jpgs/jpgs'),
                               output_path=SMALL_IMAGES_DIR,
                               scale=0.05,
                               img_filter=Image.NEAREST)

data = pd.read_csv(FINAL_TAGS_CSV, usecols=['image_id', 'washover'])

data['image'] = np.NaN
print(data)

X = list()  # The features of the data
y = None  # The labels of the data

for i, row in data.iterrows():
    print('\rLoaded %s of %s images ' % (i, len(data)) + '.' * (i % 3), end='')
    image_path = path.join(SMALL_IMAGES_DIR, row['image_id'])

    # Load a 2d array of grayscale values
    image: np.ndarray = cv2.imread(image_path, 0)

    # String each row together to form a single 1d array of features
    image = image.ravel()

    # Create a row as a DataFrame with all the features as columns
    # features: pd.DataFrame = pd.DataFrame(image.reshape(-1, len(image)))

    X.append(list(image))

print('\rLoaded all of the images!')
print(pd.DataFrame(X, columns=range(len(X[0]))))


# Split into test and training sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=SEED)
