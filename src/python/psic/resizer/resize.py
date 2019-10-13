import argparse
import os
from typing import Union

from psic import s
from psic.resizer import generate

DATA_PATH: Union[bytes, str] = os.path.abspath(s.DATA_PATH)

################################################
# Define command-line parameters and arguments #
################################################

parser = argparse.ArgumentParser(prog='resize')

parser.add_argument('--path', '-p', default=DATA_PATH,
                    help='The path on your system to set the scope of file search to (Default: %(default)s).')

parser.add_argument('--output_path', '-o', default=os.path.join(DATA_PATH, s.RESIZE_SUB_FOLDER),
                    help='The path on your system to set the output of resized images (Default: %(default)s).')

parser.add_argument('--scale', '-s', type=float, default=0.15,
                    help='The resolution in comparison to the original image to shrink the original image to. '
                         '1 = 100% of original size, 0.15 = 15% of original size, etc. (Default: %(default)s)')

parser.add_argument('--debug', '-d', action='store_true',
                    help='If included, the program will print info throughout the process (Default: %(default)s).')

# Add custom OPTIONS to the script when running command-line
OPTIONS: argparse.Namespace = parser.parse_args()

generate.resize_all_images(path=OPTIONS.path,
                           output_path=OPTIONS.output_path,
                           scale=OPTIONS.scale,
                           debug=OPTIONS.debug)
