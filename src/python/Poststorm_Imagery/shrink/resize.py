from PIL import Image
import os

# declare the size to convert the image
# size_300 = (300,300)


def search_files(directory='.', extension='G:\\Shared drives\\C-Sick\\RGB'):
    extension = extension.lower()
    for dir_path, dir_names, files in os.walk(directory):
        for name in files:
            if extension and name.lower().endswith(extension):
                print(os.path.join(dir_path, name))
            elif not extension:
                print(os.path.join(dir_path, name))


# s_path = 'G:\\Shared drives\\C-Sick\\data'
# print(os.listdir(s_path))

# go through each image in the directory and find the .jgp file and resize them and save them to folder named 'mine'
# for f in os.listdir('.'):
        #    if f.endswith('.jpg'):
        #        i = Image.open(f)
        #       fn, f_ext = os.path.splitext(f)

        #       i.thumbnail(size_300)
#     i.save('mine/{}_300{}'.format(fn, f_ext))

