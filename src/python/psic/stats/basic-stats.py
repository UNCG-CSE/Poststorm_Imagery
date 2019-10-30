import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.image as pltimg
import pandas as pd


def analyze_images(folder):
    red_list = []
    green_list = []
    blue_list = []
    for image in os.listdir(folder):
        img = pltimg.imread(os.path.join(folder, image))

        # print("Image Name: " + str(image))
        # print('Image Hight {}'.format(img.shape[0]))
        # print('Image Width {}'.format(img.shape[1]))
        # print('Image size {}'.format(img.size))
        # print('Maximum RGB value in this image {}'.format(img.max()))
        # print('Minimum RGB value in this image {}'.format(img.min()))

        # Get the average R, G, and B pixel values for this image and add to list of averages for this group of images
        red_avg = np.mean(img[:, :, 0])
        green_avg = np.mean(img[:, :, 1])
        blue_avg = np.mean(img[:, :, 2])

        red_list.append(red_avg)
        green_list.append(green_avg)
        blue_list.append(blue_avg)

        # print('Average pixel value for the Red Channel: ' + str(red_avg))
        # print('Average pixel value for the Green Channel: ' + str(green_avg))
        # print('Average pixel value for the Blue Channel: ' + str(blue_avg))
        #print('\n')

    print("Average RGB values for each image in " + folder + ': ')
    print(red_list)
    print(green_list)
    print(blue_list)
    print('\n')

    print("Total Average Red Channel Value for " + folder + ': ' + str(np.mean(red_list)))
    print("Total Average Green Channel Value for " + folder + ': ' + str(np.mean(green_list)))
    print("Total Average Blue Channel Value for " + folder + ': ' + str(np.mean(blue_list)))
    print('\n')

    df = pd.DataFrame({'x': range(1, 21), 'y1': red_list, 'y2': green_list,
                       'y3': blue_list})
    # multiple line plot
    plt.plot('x', 'y1', data=df, marker='', color='red', linewidth=2, label="red")
    plt.plot('x', 'y2', data=df, marker='', color='green', linewidth=2, label="green")
    plt.plot('x', 'y3', data=df, marker='', color='blue', linewidth=2, linestyle='dashed', label="blue")
    plt.legend()
    plt.title("RGB Values for images in " + folder)
    plt.show()


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
