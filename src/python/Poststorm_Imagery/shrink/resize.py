from pillow import Image
import os

#declair the size to convert the image
size_300 = (300, 300)

#spath = r'G:\\Shared drives\\C-Sick\\RGB'
#print(os.listdir(spath))

#go through each image in the directory and find the .jgp file and resize them and save them to folder named 'mine'
for f in os.listdir('.'):
    if f.endswith('.jpg'):
        i = Image.open(f)
        fn, fext = os.path.splitext(f)

        i.thumbnail(size_300)
        i.save('mine/{}_300{}'.format(fn, fext))
