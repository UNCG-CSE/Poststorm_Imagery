# Project Introduction

Research scientists studying the effects of storms on land in the path of travel have for a long time needed a tool 
to help make sense of images taken and analyze them for meaningful characteristics. In order for researchers to analyze 
photos of storm-related imagery, we are trying to build a program that can collect data, serve images to research teams 
in order to tag data, build classifiers for labelling whether the image contains non-coastal, coastal, or just all 
water, then from that, taking the coastal images and analyzing them further to determine whether or not there is 
wash-over, the land is developed and other characteristics important to understanding the images.

This will likely involve a long process of tagging the data and building a model that can at least get started with 
segmentation or classification. For the first part of the project, we have been dealing with the collection and 
preparation of the images for our goals.

## Member Tasks

### [**Rinty Chowdhury**](https://github.com/rintychy)  

<!-- Insert tasks here -->

---

### [**Daniel Foster**](https://github.com/dlfosterbot)  

Explored statistical analysis on the image size of Hurricane Florence coastal versus inland images and used the log
function to scale down the values. The mean of inland image sizes is greater than that of the coastal images. Plotted
histograms for each data set and fitted them with a gamma distribution using method of moments. Attempted to use MLE
and KDE but had syntax/library issues. I also ran into an issue where the classroom method for fitting the distribution
didn't scale as needed. Used another method and plotted separately. Applied two tailed z-test on coastal images to find
97.5% confidence interval. I did not have other variables to apply correlation and null hypothesis testing. After the
images are annotated, I'll return to statistical analysis of those data.
Total time spent on task: 12 hours

Developed utility that inputs a GPS coordinate and outputs the image filename(s) that contains that lat/long point.
Unlike image count script, it runs in O(n), hurray!
Time spent on task: 5 hours.

---  

### [**Matthew Moretz**](https://github.com/Matmorcat)  

<!-- Insert tasks here -->

---

### [**Shah Nafis Rafique**](https://github.com/ShahNafisRafique)  

<!-- Insert tasks here -->

---

### [**John Weber**](https://github.com/JWeb56)  

<!-- Insert tasks here -->
