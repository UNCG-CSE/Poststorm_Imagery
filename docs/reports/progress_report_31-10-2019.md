# Project Introduction

Research scientists studying the effects of storms on land in the path of travel
have for a long time needed a tool to help make sense of images taken and
analyze them for meaningful characteristics. In order for researchers to analyze
photos of storm-related imagery, we are trying to build a program that can
collect data, serve images to research teams in order to tag data, build
classifiers for labelling whether the image contains non-coastal, coastal, or
just all water, then from that, taking the coastal images and analyzing them
further to determine whether or not there is wash-over, the land is developed
and other characteristics important to understanding the images.

This will likely involve a long process of tagging the data and building a model
that can at least get started with segmentation or classification. For the first
part of the project, we have been dealing with the collection and preparation of
the images for our goals.

## Member Tasks

### [**Rinty Chowdhury**](https://github.com/rintychy)

#### 1. Find_center

Created script to find the center of an Image using the longitude and latitude of each corner. It takes four longitude of each corner and four latitude of each corner as parameter. Then it finds the midppoint of each side of the image. After that it uses those four midpoints and create two lines. Then find the intersection point of those two lines. That intersection point is the center of that image. It returns the center as tuple. Center of an image will be useful for classifier later on and any user will be able to use it to do further research on the images using center point.

**Time:** 8 - 10 hours

#### 2. Statistical analysis using Image size and resolution

For basic statistics, I calculated the mean, variance, median, and standard deviation for image size and resolution. 

For distribution modeling, I ploted the histogram and density curve using seaborn for image size and resolution. Based on the diagram the image size data fall under unimodal distribution and image resolution fall under bimodal distribution. One of them has one high peak and another has two high peaks. I also used the T-critical value to find the confidence interval for image size and resolution.

For hypothesis testing, I have seperated the data into two parts. One part contains images with 300 dpi resolution and another part contains images with 96 dpi resolution. Then I calculated the mean and standard deviation for each type of resolutions. I used two sample t-test for the hypothesis testing. Null hypothesis is checking if the image size mean is same between 300 and 96 dpi resolution images. I ploted the data and their mean together to see if the mean for both data are same or not. Then I calculated the p-value for my t-test. Since the p-value was smaller than the 95% confidence level, I rejected the null hypothesis. 

For correlation and cooveriance, I calculated the correlatio and covariance of image size and resolution. Then I ploted the data to see if their is any correlation between size and resolution. Found that their is very little position correlation between size and resolution.

**Time:** 34 - 36 hours

---

### [**Daniel Foster**](https://github.com/dlfosterbot)

Explored statistical analysis on the image size of Hurricane Florence coastal
versus inland images and used the log function to scale down the values. The
mean of inland image sizes is greater than that of the coastal images. Plotted
histograms for each data set and fitted them with a gamma distribution using
method of moments. Attempted to use MLE and KDE but had syntax/library issues. I
also ran into an issue where the classroom method for fitting the distribution
didn't scale as needed. Used another method and plotted separately. Applied two
tailed z-test on coastal images to find 97.5% confidence interval. I did not
have other variables to apply correlation and null hypothesis testing. After the
images are annotated, I'll return to statistical analysis of those data. Total
time spent on task: 15 hours
[![Source](https://img.shields.io/badge/Source-Click%20Me-informational)](
https://github.com/UNCG-CSE/Poststorm_Imagery/tree/beta/src/python/psic/Data%20Statistics)

Developed utility that inputs a GPS coordinate and outputs the image filename(s)
that contains that lat/long point. Unlike image count script, it runs in O(n),
hurray! Time spent on task: 5 hours.
[![Source](https://img.shields.io/badge/Source-Click%20Me-informational)](
https://github.com/UNCG-CSE/Poststorm_Imagery/tree/beta/src/python/psic/find_point)

---

### [**Matthew Moretz**](https://github.com/Matmorcat)

#### 1. Collector

Improving the collector script and making sure that some edge cases
(like the remote server returning a redirect work)

[![Documentation](https://img.shields.io/badge/Documentation-Click%20Me-brightgreen)](
https://post-storm-imagery.readthedocs.io/en/latest/collector/)
[![Source](https://img.shields.io/badge/Source-Click%20Me-informational)](
https://github.com/UNCG-CSE/Poststorm_Imagery/tree/master/src/python/psic/collector)

**Time:** 50 hours

#### 2. Cataloging

Create a cataloging script to aggregate data such as geo-spacial data like latitudes and longitudes from the
individual `.geom` files as well as checksums (`catalog_v2` branch) and actually run these scripts to generate the
files for storms from 2018 to 2019. This includes documentation and examples of usage

[![Documentation](https://img.shields.io/badge/Documentation-Click%20Me-brightgreen)](
https://post-storm-imagery.readthedocs.io/en/latest/cataloging/)
[![Source](https://img.shields.io/badge/Source-Click%20Me-informational)](
https://github.com/UNCG-CSE/Poststorm_Imagery/tree/master/src/python/psic/cataloging)

**Time:** 90 hours

#### 3. Assigner

A back-end python system for handling the tagging of images. This script handles a set of queues that store
references to images that are either ready to be tagged, completely tagged, or skipped too often. The assigner
randomly chooses an image and assigns it to a user when a person starts tagging a new image. Once an image is tagged
more than once

![Documentation](https://img.shields.io/badge/Documentation-Not%20Added%20Yet-inactive)
[![Source](https://img.shields.io/badge/Source-Click%20Me-informational)](
https://github.com/UNCG-CSE/Poststorm_Imagery/tree/master/src/python/psic/assigner)

**Time:** 50 hours


#### 4. Misc

I've been working on structuring of the repository and also looking into different strategies to handle the image
data and the best way to work with it. I've also been tweaking everything, including other scripts to make them
pretty and working with Nafis to get the dashboard working.

**Time:** *too much*



---

### [**Shah Nafis Rafique**](https://github.com/ShahNafisRafique)

**Hours spent:** A lot 😢, 8 to 13 to 20 per week depending on the week.


#### Dashboard

[![Documentation](https://img.shields.io/badge/Documentation-Click%20Me-brightgreen)](
https://post-storm-imagery.readthedocs.io/en/latest/dashboard/)

1. Added user authentication with Auth0 service.

2. As a result remade the entire dashboard from scratch to incorporate the
   authentication. Made sure protected links would only allowed logged in users.

3. Added endpoint to call python script to get the image a specific user is
   supposed to tag.

4. Added endpoint to call python script to skip an image.

5. Added endpoint to call python script to tag an image as an ocean and get the
   next image to tag.

6. Added endpoint to call python script to tag an image with the data from the
   form and get the next image to tag.

7. Added package.json scripts to build the web-server for production

Tasks 1-2 took about 3 weeks.
Tasks 3-7 took the last 3 weeks.

---

### [**John Weber**](https://github.com/JWeb56)
#### 1.  Creating/configuring VM and Google Cloud Storage

I purchased a free account on Google Cloud and created a project for our 405 project.
I initialized and configured a VM instance on which we will ultimately house our tagging apparatus
and our web server, so taggers can access our dashboard via the web. Also, in order to allow for
quick and efficient serving of images to our front-end, I purchased a storage bucket and uploaded
all of the images which we want to tag (four or five archives from Florence) and uploaded all of the
full-sized images to the bucket. In order to access the images from our VM, I had to spend
a good amount of time with configuring access to the different APIs and mounting the bucket to the
VM file system. I also set up a local MySQL server to store the tagged image info, but we didn't end up
using that.


**Time:** 25 hours

#### 2.  Attempting to create a NodeJS apparatus for storing tagged image information

Originally, it was my task to save the tagged image information, passed from the NodeJS front-end,
to the MySQL database. However, it was determined that the back-end should be written in python and this was eventually
passed to another group member.


**Time:** 5 hours

#### 3.  Analyzing image pixel values and performing basic statistics

I gathered 60 Florence images (20 each from inland, ocean, and shoreline classes) and analyized their RGB
pixel values in order to determine if there are any simple statistical measures (mean values, standard deviations
between RGB channels, etc.) by which we might distinguish these different types of images.
This involved writing scripts to calculate the average pixel values for RGB channels across multiple directories
of images, plotting charts to show the differences between channels for all images, concatenating images,
converting images to grayscale, and fitting normal distributions to the histograms of these
images in order to make inferences about image groups based on statistical measures such as mean
and standard deviation. I then constructed confidence intervals to determine whether to accept or reject the
hypothesis that the mean differences observed across the different classes of images was statistically significant
and as such, a simple classifier could use these differences in order to label images with at least an acceptable
level of accuracy.


[![Source](https://img.shields.io/badge/Source-Click%20Me-informational)](
https://github.com/UNCG-CSE/Poststorm_Imagery/tree/master/src/python/psic/stats)

**Time:** 30 hours

#### 4.  Providing a sample or template for training Convolutional Neural Network

Since our ultimate goal is to train a convolutional neural network to classify our images based on a certain
number of classes/labels, but we still have not completed the tagging of our images, I wanted to
provide a sample script which shows how to train and test a neural network model. The example I provided was largely
taken from an example provided by keras/tensorflow, and trains a network to classify/recognize
a set of images taken from a fashion dataset. Hopefully this will serve as a reference for group members
as we progess into the next stage of our project.


[![Source](https://img.shields.io/badge/Source-Click%20Me-informational)](
https://github.com/UNCG-CSE/Poststorm_Imagery/tree/master/src/python/psic/cnn_model)

**Time:** 1-2 hours
