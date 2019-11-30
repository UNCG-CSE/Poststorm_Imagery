import pandas as pd
from pathlib import Path
import os

#Counts images for each storm, creates a dataframe and visualization.
storm_count= {}
images_path = "G:/Shared drives/P-Sick/data"
path_list = Path(images_path)
total_count = 0
jpg_count = 0
dirs = os.listdir(path_list)
dictOfWords = { i : 0 for i in dirs }

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
                            total_count+=1
                            jpg_count += 1
                            dictOfWords[dir] = jpg_count

    jpg_count = 0
print(dictOfWords)
print(total_count)

x = pd.DataFrame(list(dictOfWords.items()), index=['a', 'b', 'c', 'd', 'e'])
x.hist(bins=5)
