from typing import Tuple, Union
from PIL import Image
from src.python.Poststorm_Imagery.collector import s
import os

# Declare the scale factor
SIZE_SCALE = 0.15  # 1 = 100% of original size, 0.15 = 15% of original size, etc.

# Declare the folder path
DATA_PATH: Union[bytes, str] = os.path.abspath(s.DATA_PATH)
TAR_CACHE_PATH: Union[bytes, str] = os.path.join(DATA_PATH, s.TAR_CACHE)

# Empty file to store all the jpg files
files = []

# Loop through the path and find all the jpg files
# r = root, d = directories, walk_f = files
for r, d, walk_f in os.walk(TAR_CACHE_PATH):
    # get the all the file in walk_f
    for file in walk_f:
        # add the file to 'filePath'
        filePath = os.path.join(r, file)
        # iterate through the path to find all the jpgs and ignore all the corrupted files
        if '.jpg' in file and os.path.getsize(filePath) > 0:
            # add the jpg file to 'filePath'
            files.append(filePath)

    # Resize all the jpg files and save it to the appropriate sub-folder
    index = 0
    for f in files:
        index += 1
        # print files
        print(f)
        # open file as Image
        i = Image.open(f)
        # Get the original image's width and height
        w, h = i.size
        # Reduce the size of the original image by a specified multiplier (scale factor)
        new_size: Tuple = (int(w * SIZE_SCALE), int(h * SIZE_SCALE))
        # split the file name and file extension
        fn, f_ext = os.path.splitext(f)
        # resize the Image based on given scale factor
        i = i.resize(new_size, Image.ANTIALIAS)
        # get the base name from the 'fileName'.
        fileName = os.path.basename(f)
        # rename the file by replaceing the word 'data' with 'smallerJPG'
        newFileName = f.replace("data", "smallerJPG")
        # get the directory of the 'newFileName'
        directory = os.path.dirname(newFileName) + "\\"
        # check if the directory already exists given by the 'directory' field
        if not os.path.exists(directory):
            # make the directory
            os.makedirs(directory)
        # save the Image to the specified directory with the given fileName
        i.save(directory + fileName)
        file = []
