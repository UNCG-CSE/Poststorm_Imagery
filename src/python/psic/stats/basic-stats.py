import imageio
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import imageio
import numpy as np

import os
import matplotlib.image as pltimg

def view_images(folder):
    for image in os.listdir(folder):
        img = pltimg.imread(os.path.join(folder, image))
        plt.figure()
        plt.imshow(img)
        plt.title("Original Image")
        plt.axis('off')

        ## Negative of Image
        negative = 255 - img  # neg = (L-1) - img

        plt.figure(figsize=(6, 6))
        plt.imshow(negative);
        plt.title("Negative Image")
        plt.axis('off');


        # Gamma encoding
        ## pic = imageio.imread('img/parrot.jpg')
        gamma = 2.2  # Gamma < 1 ~ Dark ; Gamma > 1 ~ Bright

        gamma_correction = ((img / 255) ** (1 / gamma))
        plt.figure(figsize=(5, 5))
        plt.title("Gamma Corrected Image")
        plt.imshow(gamma_correction)
        plt.axis('off');
        plt.show()

view_images('data/test_inland_images')
