from pathlib import Path
from GPSPhoto import gpsphoto
import os
import csv

#Iterates through a directory, locates jpgs, and extracts GPS coordinates. Places all jpg coordintes into
#a csv in that same image directory.

images_path = "G:/Shared drives/C-Sick/data"
path_list = Path(images_path)
dirs = os.listdir(path_list)
storm_images = {i: 0 for i in dirs}
gps_coord = {}

#writes stores GPS coord dictionary into csv
def csvWrites(jpgs, gps_coord):
    with open(str(jpgs + '/gps_coords.csv'), 'w') as csvfile:
        writer = csv.writer(csvfile)
        for key, value in gps_coord.items():
            writer.writerow([key, value])

for dir in os.listdir(path_list):
    storm = os.path.join(path_list, dir)
    for subdir in os.listdir(storm):
        storm_folder = os.path.join(storm,subdir)
        if os.path.isdir(storm_folder):
            for jpg_file in os.listdir(storm_folder):
                jpgs = os.path.join(storm_folder, jpg_file)
                if os.path.isdir(jpgs):
                    for file in os.listdir(jpgs):
                        if file.endswith(".jpg"):
                            gps_coord[file] = gpsphoto.getGPSData(str(jpgs+ '/'+ file))

                    csvWrites(jpgs, gps_coord)



