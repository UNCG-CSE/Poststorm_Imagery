from PIL import Image
import os

#declair the size to convert the image
#size_300 = (300,300)


def search_files(directory='.', extension='G:\\Shared drives\\C-Sick\\RGB'):
    extension = extension.lower()
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            if extension and name.lower().endswith(extension):
                print(os.path.join(dirpath, name))
            elif not extension:
                print(os.path.join(dirpath, name))



#spath = r'G:\\Shared drives\\C-Sick\\data'
#print(os.listdir(spath))

#go through each image in the directory and find the .jgp file and resize them and save them to folder named 'mine'
#for f in os.listdir('.'):
        #    if f.endswith('.jpg'):
        #        i = Image.open(f)
        #       fn, fext = os.path.splitext(f)

        #       i.thumbnail(size_300)
#     i.save('mine/{}_300{}'.format(fn, fext))

