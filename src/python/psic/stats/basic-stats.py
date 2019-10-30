import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.image as pltimg

def analyze_images(folder):
    for image in os.listdir(folder):
        img = pltimg.imread(os.path.join(folder, image))

        print("Image Name: " + str(image))
        print('Image Hight {}'.format(img.shape[0]))
        print('Image Width {}'.format(img.shape[1]))
        print('Image size {}'.format(img.size))
        print('Maximum RGB value in this image {}'.format(img.max()))
        print('Minimum RGB value in this image {}'.format(img.min()))
        print('Average pixel value for the Red Channel: ' + str(np.mean(img[:, :, 0])))
        print('Average pixel value for the Green Channel: ' + str(np.mean(img[:, :, 1])))
        print('Average pixel value for the Blue Channel: ' + str(np.mean(img[:, :, 2])))

def plot_images(folder):
    for image in os.listdir(folder):
        img = pltimg.imread(os.path.join(folder, image))

        ## Original Image
        plt.figure()
        plt.imshow(img)
        plt.title("Original Image")
        plt.axis('off')

        # ## Negative of Image
        # negative = 255 - img  # neg = (L-1) - img
        #
        # plt.figure(figsize=(6, 6))
        # plt.imshow(negative);
        # plt.title("Negative Image")
        # plt.axis('off');
        #
        #
        # # Gamma encoding
        # ## pic = imageio.imread('img/parrot.jpg')
        # gamma = 2.2  # Gamma < 1 ~ Dark ; Gamma > 1 ~ Bright
        #
        # gamma_correction = ((img / 255) ** (1 / gamma))
        # plt.figure(figsize=(5, 5))
        # plt.title("Gamma Corrected Image")
        # plt.imshow(gamma_correction)
        # plt.axis('off');
        # plt.show()


        ## Grayscale
        gray = lambda rgb: np.dot(rgb[..., :3], [0.299, 0.587, 0.114])
        gray = gray(img)
        plt.figure()
        plt.title("Grayscale Image")
        plt.imshow(gray, cmap=plt.get_cmap(name='gray'))
        plt.show()

analyze_images('data/test_inland_images')
analyze_images('data/test_ocean_images')
analyze_images('data/test_shoreline_images')
