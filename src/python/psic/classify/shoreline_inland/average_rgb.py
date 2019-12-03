#def pixel returns either the green or blue average pixel value and writes the values to a csv
import os
from pathlib import Path

import cv2
import numpy as np

inland_images = {}
shoreline_images = {}
green = {}
blue = {}

print(inland_images)
inland_images_path = Path("G:/Shared drives/P-Sick/data/Florence/20180922a_jpgs/training_inland")

shoreline_images_path = Path("G:/Shared drives/P-Sick/data/Florence/20180917a_jpgs/training_shoreline")

def pixel(folder):
    i = 0
    for file in os.listdir(folder):
        if file.endswith(".jpg"):
            jpg = os.path.join(folder, file)
            jpg = cv2.imread(jpg)
            green_avg = np.mean(jpg[:, :, 1])
            green[i] = green_avg
            #blue_avg = np.mean(jpg[:, :, 2])
            #blue[i] = blue_avg
            i = i+1
    return green
#shoreline_images = pixel(shoreline_images_path)
inland_images = pixel(inland_images_path)
#with open('shoreline_green.csv', 'w') as f:
#    for key in shoreline_images.keys():
#        f.write("%s,%s\n"%(key,shoreline_images[key]))

with open('inland_green.csv', 'w') as f:
    for key in inland_images.keys():
        f.write("%s,%s\n" % (key, inland_images[key]))
