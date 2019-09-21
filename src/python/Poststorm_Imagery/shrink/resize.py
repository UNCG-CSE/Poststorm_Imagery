from PIL import Image
import os

"""
#creates all folders
os.makedirs('G:\Shared drives\C-Sick\smallerJPGImage')
os.makedirs('G:\Shared drives\C-Sick\smallerJPGImage\Barry')
os.makedirs('G:\Shared drives\C-Sick\smallerJPGImage\Dorian')
os.makedirs('G:\Shared drives\C-Sick\smallerJPGImage\Florence')
os.makedirs('G:\Shared drives\C-Sick\smallerJPGImage\Gordon')
os.makedirs('G:\Shared drives\C-Sick\smallerJPGImage\Michael')
"""

# declair the size to convert the image
size_300 = (300, 300)

#declair the path
path = 'G:\\Shared drives\\C-Sick\\data\\'

#empty file to store all the jpg files
files = []

#loop through the path and find all the jpg files
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        filePath = os.path.join(r, file)
        if '.jpg' in file and os.path.getsize(filePath) > 0:
            files.append(filePath)

#resize all the jpg files and save it to the appropiate folder
    index = 0
    for f in files:
        index += 1
        print(f)
        #save all the Barry images to the Barry folder
        if f.startswith('G:\\Shared drives\\C-Sick\\data\\Barry'):
            i = Image.open(f)
            fn, fext = os.path.splitext(f)
            i = i.resize(size_300, Image.ANTIALIAS)
            path = 'G:\\Shared drives\\C-Sick\\smallerJPGImage\\Barry\\'
            fileName = os.path.basename(f)
            name = 'Barry' + fileName
            i.save(path + name)
        #save all the Dorian images to the Dorian folder
        elif f.startswith('G:\\Shared drives\\C-Sick\\data\\Dorian'):
            i = Image.open(f)
            fn, fext = os.path.splitext(f)
            i = i.resize(size_300, Image.ANTIALIAS)
            path = 'G:\\Shared drives\\C-Sick\\smallerJPGImage\\Dorian\\'
            fileName = os.path.basename(f)
            name = 'Dorian' + fileName
            i.save(path + name)
        #save all the Florence images to the Florence folder
        elif f.startswith('G:\\Shared drives\\C-Sick\\data\\Florence'):
            i = Image.open(f)
            fn, fext = os.path.splitext(f)
            i = i.resize(size_300, Image.ANTIALIAS)
            path = 'G:\\Shared drives\\C-Sick\\smallerJPGImage\\Florence\\'
            fileName = os.path.basename(f)
            name = 'Florence' + fileName
            i.save(path + name)
        #save all the Gordon images to the Gordon folder
        elif f.startswith('G:\\Shared drives\\C-Sick\\data\\Gordon'):
            i = Image.open(f)
            fn, fext = os.path.splitext(f)
            i = i.resize(size_300, Image.ANTIALIAS)
            path = 'G:\\Shared drives\\C-Sick\\smallerJPGImage\\Gordon\\'
            fileName = os.path.basename(f)
            name = 'Gordon' + fileName
            i.save(path + name)
        #save all the Michael images to the Michael folder
        elif f.startswith('G:\\Shared drives\\C-Sick\\data\\Michael'):
            i = Image.open(f)
            fn, fext = os.path.splitext(f)
            i = i.resize(size_300, Image.ANTIALIAS)
            path = 'G:\\Shared drives\\C-Sick\\smallerJPGImage\\Michael\\'
            fileName = os.path.basename(f)
            name = 'Michael' + fileName
            i.save(path + name)
