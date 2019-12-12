import os

import cv2
import matplotlib.image as plt_img
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
# import pandas as pd
from PIL import Image
from scipy.stats import norm

red_super_list = []
green_super_list = []
blue_super_list = []


def analyze_images(folder):
    red_list = []
    green_list = []
    blue_list = []
    for image in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, image))
        # plt.calcHist([img], [0], None, [256], [0, 256])
        # plt.show()
        # img = plt_img.imread(os.path.join(folder, image))

        # print("Image Name: " + str(image))
        # print('Image Height {}'.format(img.shape[0]))
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

        #print('Average pixel value for the Red Channel: ' + str(red_avg))
        # print('Average pixel value for the Green Channel: ' + str(green_avg))
        # print('Average pixel value for the Blue Channel: ' + str(blue_avg))
        # print('\n')

    # print("Average RGB values for each image in " + folder + ': ')
    # print(red_list)
    # print(green_list)
    # print(blue_list)
    # print('\n')
    #
    print("Total Average Red Channel Value for " + folder + ': ' + str(np.mean(red_list)))
    print("Total Average Green Channel Value for " + folder + ': ' + str(np.mean(green_list)))
    print("Total Average Blue Channel Value for " + folder + ': ' + str(np.mean(blue_list)))
    print('\n')
    #
    # red_super_list.append(np.mean(red_list))
    # green_super_list.append(np.mean(green_list))
    # blue_super_list.append(np.mean(blue_list))

    # df = pd.DataFrame({'x': range(1, 21), 'y1': red_list, 'y2': green_list,
    #                    'y3': blue_list})
    # # multiple line plot
    # plt.plot('x', 'y1', data=df, marker='', color='red', linewidth=2, label="red channel")
    # plt.plot('x', 'y2', data=df, marker='', color='green', linewidth=2, label="green channel")
    # plt.plot('x', 'y3', data=df, marker='', color='blue', linewidth=2, linestyle='dashed', label="blue channel")
    # plt.title("RGB Values for images in " + folder)
    # plt.show()


def plot_images(folder):
    for image in os.listdir(folder):
        img = plt_img.imread(os.path.join(folder, image))

        # Original Image
        plt.figure()
        plt.imshow(img)
        plt.title("Original Image (1549x1164)")
        plt.axis('off')

        # Negative of Image
        negative = 255 - img  # neg = (L-1) - img

        plt.figure(figsize=(6, 6))
        plt.imshow(negative)
        plt.title("Negative Image")
        plt.axis('off')

        # Gamma encoding
        # pic = imageio.imread('img/parrot.jpg')
        gamma = 2.2  # Gamma < 1 ~ Dark ; Gamma > 1 ~ Bright

        gamma_correction = ((img / 255) ** (1 / gamma))
        plt.figure(figsize=(5, 5))
        plt.title("Gamma Corrected Image")
        plt.imshow(gamma_correction)
        plt.axis('off')
        plt.show()

        # Grayscale
        gray = lambda rgb: np.dot(rgb[..., :3], [0.299, 0.587, 0.114])
        gray = gray(img)
        plt.figure()
        plt.title("Grayscale Image (1549x1164)")
        plt.imshow(gray, cmap=plt.get_cmap(name='gray'))
        plt.show()


# This function generates a histogram from a grayscale image, fits a normal distribution to the data and shows the
# critical variables mu and sigma
def grayscale_image_histogram(file):
    img = cv2.imread(file, 0)

    # Convert image to vector
    vector = img.ravel()

    # best fit of normal distribution to image vector
    (mu, sigma) = norm.fit(vector)

    # the histogram of the image data
    n, bins, patches = plt.hist(vector, 256, density=1, facecolor='green', alpha=0.75)

    # add a 'best fit' line
    y = norm.pdf(bins, mu, sigma)
    plt.plot(bins, y, 'r--', linewidth=2)

    # plot
    plt.xlabel('Pixel Value')
    plt.ylabel('Probability')
    plt.title(r'$\mathrm{Histogram\ of\ Ocean\ Images:}\ \mu=%.3f,\ \sigma=%.3f$' % (mu, sigma))
    plt.grid(True)

    plt.show()


def image_t_test(file1, file2):
    img1 = cv2.imread(file1, 0)
    img2 = cv2.imread(file2, 0)

    vector1 = img1.ravel()
    vector2 = img2.ravel()

    # 2-sided t-test
    print(stats.ttest_ind(vector1, vector2, False))


# This function horizontally concatenates every image in the specified directory
def concat_images(folder):
    images = [Image.open(os.getcwd() + '/' + folder + '/' + x) for x in os.listdir(folder)]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    new_im.save(folder + '/concat.jpg')


# def blue_histogram(file):
#     img = cv2.imread(file)
#     blue_values = np.hstack(img[:, :, 0])

    # # best fit of normal distribution to image vector
    # (mu, sigma) = norm.fit(blue_values)
    #
    # # the histogram of the image data
    # n, bins, patches = plt.hist(blue_values, 256, density=1, facecolor='blue', alpha=0.75)
    #
    # # add a 'best fit' line
    # y = norm.pdf(bins, mu, sigma)
    # plt.plot(bins, y, 'r--', linewidth=2)
    #
    # # plot
    # plt.xlabel('Pixel Value')
    # plt.ylabel('Probability')
    # plt.title(r'$\mathrm{Blue\ Channel\ Values\ For\ Shoreline\ Images:}\ \mu=%.3f,\ \sigma=%.3f$' % (mu, sigma))
    # plt.grid(True)
    #
    # plt.show()


# This function takes in all of the images of the input directory and performs a pixel-by-pixel average of RGB values
def average_images(folder):
    # Access all img files in directory
    imlist = os.listdir(os.getcwd() + '/' + folder)

    # Input dimensions of images (all same size, since compressed) and n = num of images per folder
    w, h = 1549, 1164
    n = 20

    # Create a numpy array of floats to store the RGB values
    arr = np.zeros((h, w, 3), np.float)

    # Average pixel values
    for im in imlist:
        imgarr = np.array(Image.open(os.getcwd() + '/' + folder + '/' + im), dtype=np.float)
        print(imgarr.shape)
        arr = arr + imgarr / n

    # Round values in array and cast as 8-bit integer
    arr = np.array(np.round(arr), dtype=np.uint8)

    # Generate, save and preview final image
    print(arr.shape)
    first = np.mean(arr[0])
    second = np.mean(arr[1])
    third = np.mean(arr[2])

    average = (first + second + third) / 3
    print(average)
    out = Image.fromarray(arr, mode="RGB")
    out.show()


analyze_images('data/test_inland_images')
# analyze_images('data/test_ocean_images')
# analyze_images('data/test_shoreline_images')
# analyze_images('data/test_inland_images')
# analyze_images('data/test_ocean_images')
# analyze_images('data/test_shoreline_images')
#
# df = pd.DataFrame({'x': range(1, 4), 'y1': red_super_list, 'y2': green_super_list,
#                        'y3': blue_super_list})
# # multiple line plot
# plt.plot('x', 'y1', data=df, marker='', color='red', linewidth=2, label="red channel")
# plt.plot('x', 'y2', data=df, marker='', color='green', linewidth=2, label="green channel")
# plt.plot('x', 'y3', data=df, marker='', color='blue', linewidth=2, linestyle='dashed', label="blue channel")
# plt.title("Total average pixel values by channel")
# plt.show()
#
#
# print("Average Red Channel Values for Inland, Ocean, Shoreline images: {}" .format(red_super_list))
# print("Average Green Channel Values for Inland, Ocean, Shoreline images: {}" .format(green_super_list))
# print("Average Blue Channel Values for Inland, Ocean, Shoreline images: {}" .format(blue_super_list))

# concat_images('data/test_inland_images')
# concat_images('data/test_ocean_images')
# concat_images('data/test_shoreline_images')

# # Generate histograms for the concatenated (sum of all images) images in each directory
# grayscale_image_histogram('data/test_inland_images/concat.jpg')
# grayscale_image_histogram('data/test_ocean_images/concat.jpg')
# grayscale_image_histogram('data/test_shoreline_images/concat.jpg')
# blue_histogram('data/test_inland_images/concat.jpg')
# blue_histogram('data/test_ocean_images/concat.jpg')
# blue_histogram('data/test_shoreline_images/concat.jpg')
