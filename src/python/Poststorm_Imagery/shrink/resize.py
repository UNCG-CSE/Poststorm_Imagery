from typing import Tuple
from PIL import Image
import os

# Declare the scale factor
SIZE_SCALE = 0.15  # 1 = 100% of original size, 0.15 = 15% of original size, etc.

# Declare the path
path = 'G:\\Shared drives\\C-Sick\\data\\'

# Empty file to store all the jpg files
files = []

# Loop through the path and find all the jpg files
# r = root, d = directories, walk_f = files
for r, d, walk_f in os.walk(path):
    for file in walk_f:
        filePath = os.path.join(r, file)
        if '.jpg' in file and os.path.getsize(filePath) > 0:
            files.append(filePath)

    # Resize all the jpg files and save it to the appropriate folder
    index = 0
    for f in files:
        index += 1
        print(f)
        i = Image.open(f)
        # Get the original image's width and height
        w, h = i.size
        # Reduce the size of the original image by a specified multiplier (scale factor)
        new_size: Tuple = (int(w * SIZE_SCALE), int(h * SIZE_SCALE))
        fn, f_ext = os.path.splitext(f)
        i = i.resize(new_size, Image.ANTIALIAS)
        # save it to the directory
        fileName = os.path.basename(f)
        name = fileName
        newName = f.replace("data", "smallerJPG")
        print(newName)
        directory = os.path.dirname(newName)
        if not os.path.exists(directory):
            os.makedirs(directory)
            mine = os.path.dirname(directory)
            i.save(mine + name)

    file = []
