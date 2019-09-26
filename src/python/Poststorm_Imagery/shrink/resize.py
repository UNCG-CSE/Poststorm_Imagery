from typing import Tuple

from PIL import Image
import os

"""
#creates all folders
os.makedirs('G:\\Shared drives\\C-Sick\\smallerJPGImage')
os.makedirs('G:\\Shared drives\\C-Sick\\smallerJPGImage\\Barry')
os.makedirs('G:\\Shared drives\\C-Sick\\smallerJPGImage\\Dorian')
os.makedirs('G:\\Shared drives\\C-Sick\\smallerJPGImage\\Florence')
os.makedirs('G:\\Shared drives\\C-Sick\\smallerJPGImage\\Gordon')
os.makedirs('G:\\Shared drives\\C-Sick\\smallerJPGImage\\Michael')
"""

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

        # Save all the Barry images to the Barry folder
        if f.startswith('G:\\Shared drives\\C-Sick\\data\\Barry'):
            fn, f_ext = os.path.splitext(f)
            i = i.resize(new_size, Image.ANTIALIAS)
            path = 'G:\\Shared drives\\C-Sick\\smallerJPGImage\\Barry\\'
            fileName = os.path.basename(f)
            name = fileName
            i.save(path + name)
        # Save all the Dorian images to the Dorian folder
        elif f.startswith('G:\\Shared drives\\C-Sick\\data\\Dorian'):
            fn, f_ext = os.path.splitext(f)
            i = i.resize(new_size, Image.ANTIALIAS)
            path = 'G:\\Shared drives\\C-Sick\\smallerJPGImage\\Dorian\\'
            fileName = os.path.basename(f)
            name = fileName
            i.save(path + name)
        # Save all the Florence images to the Florence folder
        elif f.startswith('G:\\Shared drives\\C-Sick\\data\\Florence'):
            fn, f_ext = os.path.splitext(f)
            i = i.resize(new_size, Image.ANTIALIAS)
            path = 'G:\\Shared drives\\C-Sick\\smallerJPGImage\\Florence\\'
            fileName = os.path.basename(f)
            name = fileName
            i.save(path + name)
        # Save all the Gordon images to the Gordon folder
        elif f.startswith('G:\\Shared drives\\C-Sick\\data\\Gordon'):
            fn, f_ext = os.path.splitext(f)
            i = i.resize(new_size, Image.ANTIALIAS)
            path = 'G:\\Shared drives\\C-Sick\\smallerJPGImage\\Gordon\\'
            fileName = os.path.basename(f)
            name = fileName
            i.save(path + name)
        # Save all the Michael images to the Michael folder
        elif f.startswith('G:\\Shared drives\\C-Sick\\data\\Michael'):
            fn, f_ext = os.path.splitext(f)
            i = i.resize(new_size, Image.ANTIALIAS)
            path = 'G:\\Shared drives\\C-Sick\\smallerJPGImage\\Michael\\'
            fileName = os.path.basename(f)
            name = fileName
            i.save(path + name)

        files = []
