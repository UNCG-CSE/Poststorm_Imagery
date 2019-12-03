import os
from typing import Tuple, Union, List

from PIL import Image

from psic import s
from psic.common import h


class ResizeImages:

    @staticmethod
    def resize_all_images(path: Union[bytes, str], output_path: Union[bytes, str], scale: float or None = 0.15,
                          new_res: Tuple[int, int] or None = None, img_filter=Image.ANTIALIAS, save: bool = True,
                          debug: bool = s.DEFAULT_DEBUG) -> list:

        # Get all jpg files
        files: List[str] = h.all_files_recursively(root_path=path, require_geom=True, file_extension='jpg', debug=debug)

        new_images: List[Image] = list()

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
                    print('\rResizing file %d of %d (%.2f%%): %s ... ' % (i, len(files), done_ratio * 100, file),
                          end='')

                # Open file as an image
                original_image = Image.open(original_abs_path)

                # Resize the image based on given scale factor
                try:

                    new_image = ResizeImages.resize_image(original_image=original_image, scale=scale,
                                                          new_res=new_res, img_filter=img_filter)
                    new_images.append(new_image)

                    if save:
                        # Get the path for the new (smaller) image without the file's name & extension in it
                        new_abs_dir = os.path.split(new_abs_path)[0]

                        # Check to make sure that the appropriate directories exist
                        if not os.path.exists(new_abs_dir):
                            os.makedirs(new_abs_dir)

                        # Save the new image to the specified directory
                        new_image.save(new_abs_path)

                except Exception as e:
                    h.print_error('\n' + str(e) + '\nThere was an OS error with resizing the image. File may be open or '
                                  'corrupted ... skipping!')

        return new_images

    @staticmethod
    def resize_image(original_image: Image, scale: float or None = 0.15,
                     new_res: Tuple[int, int] or None = None, img_filter=Image.ANTIALIAS) -> Image:
        # Get the original image's width and height
        width, height = original_image.size

        new_size: Tuple[int, int]

        if new_res is not None:
            new_size: Tuple = new_res
        elif scale is not None:
            # Reduce the size of the original image by a specified multiplier (scale factor)
            new_size: Tuple = (int(width * scale), int(height * scale))
        else:  # pragma: no cover
            raise ValueError('Neither a scale factor or new resolution was specified for resizing!')

        try:
            return original_image.resize(new_size, img_filter)

        except Exception as e:
            h.print_error(e)

    @staticmethod
    def resize_image_at_path(original_path: Union[bytes, str], small_path: Union[bytes, str],
                             scale: float or None = 0.15, new_res: Tuple[int, int] or None = None) -> bool:
        """
        Takes in an absolute path to an image file and resizes it and saves it to the specified small image path.

        :param original_path: The path to the full size image to compress
        :param small_path: The path to the resized image
        :param scale: The scale factor to reduce the image to (0.15 = 15% of the full image size)
        :param new_res: The absolute resolution to resize the image to in pixels (width x height)
        :return: Whether (True) or not (False) the image was resized successfully (some images may not be able to)
        """

        try:
            # Open file as an image
            original_image = Image.open(original_path)

            # Resize the image based on given scale factor
            new_image = ResizeImages.resize_image(original_image=original_image, scale=scale, new_res=new_res)

            # Get the path for the new (smaller) image without the file's name & extension in it
            new_abs_dir = os.path.split(small_path)[0]

            # Check to make sure that the appropriate directories exist
            if not os.path.exists(new_abs_dir):
                os.makedirs(new_abs_dir)

            # Save the new image to the specified directory
            new_image.save(small_path)
            return True

        except (IOError, OSError):
            return False
