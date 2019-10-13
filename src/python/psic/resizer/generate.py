import os
from typing import Tuple, Union, List

from PIL import Image
import auger

from psic import s, h


def resize_all_images(path: Union[bytes, str], output_path: Union[bytes, str], scale: float, **kwargs):

    # Enable debugging flag (True = output debug statements, False = don't output debug statements)
    debug: bool = (kwargs['debug'] if 'debug' in kwargs else s.DEFAULT_DEBUG)

    # Get all jpg files
    files: List[str] = h.all_files_recursively(root_path=path, file_extension='jpg', **kwargs)

    # An index for the current file for output
    i = 0

    # Loop through the path and find all the jpg files
    for file in files:
        i += 1

        # Get the files' absolute paths
        original_abs_path = os.path.join(path, file)
        new_abs_path = os.path.join(output_path, file)

        # Skip over existing compressed files
        if os.path.exists(new_abs_path) is False:

            if debug:
                done_ratio = i / len(files)
                print('\rResizing file %d of %d (%.2f%%): %s ... ' % (i, len(files), done_ratio * 100, file), end='')

            # Open file as an image
            original_image = Image.open(original_abs_path)

            # Resize the image based on given scale factor
            try:

                # Get the path for the new (smaller) image without the file's name & extension in it
                new_abs_dir = os.path.split(new_abs_path)[0]

                # Check to make sure that the appropriate directories exist
                if not os.path.exists(new_abs_dir):
                    os.makedirs(new_abs_dir)

                # Save the new image to the specified directory
                resize_image(original_image=original_image, scale=scale).save(new_abs_path)

            except Exception as e:
                h.print_error('\n' + str(e) + '\nThere was an OS error with resizing the image. File may be open or '
                              'corrupted ... skipping!')


def resize_image(original_image: Image, scale: float) -> Image:

    # Get the original image's width and height
    width, height = original_image.size

    # Reduce the size of the original image by a specified multiplier (scale factor)
    new_size: Tuple = (int(width * scale), int(height * scale))

    try:
        return original_image.resize(new_size, Image.ANTIALIAS)

    except Exception as e:
        h.print_error(e)


if __name__ == "__main__":
    with auger.magic([]):
        resize_all_images('src/python/psic/tests/resize/input',
                          'src/python/psic/tests/resize/output',
                          scale=0.15,
                          debug=True)
