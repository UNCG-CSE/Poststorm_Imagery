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

1.  Collector

    Improving the collector script and making sure that some edge cases 
    (like the remote server returning a redirect work)

    [![Documentation](https://img.shields.io/badge/Documentation-Click%20Me-brightgreen)](
    https://post-storm-imagery.readthedocs.io/en/latest/collector/)
    [![Source](https://img.shields.io/badge/Source-Click%20Me-informational)](
    https://github.com/UNCG-CSE/Poststorm_Imagery/tree/master/src/python/psic/collector)
    
    **Time:** 50 hours
   
2.  Cataloging

    Create a cataloging script to aggregate data such as geo-spacial data like latitudes and longitudes from the
    individual `.geom` files as well as checksums (`catalog_v2` branch) and actually run these scripts to generate the
    files for storms from 2018 to 2019. This includes documentation and examples of usage

    [![Documentation](https://img.shields.io/badge/Documentation-Click%20Me-brightgreen)](
    https://post-storm-imagery.readthedocs.io/en/latest/cataloging/)
    [![Source](https://img.shields.io/badge/Source-Click%20Me-informational)](
    https://github.com/UNCG-CSE/Poststorm_Imagery/tree/master/src/python/psic/cataloging)
    
    **Time:** 125 hours
   
3.  Assigner

    A back-end python system for handling the tagging of images. This script handles a set of queues that store
    references to images that are either ready to be tagged, completely tagged, or skipped too often. The assigner
    randomly chooses an image and assigns it to a user when a person starts tagging a new image. Once an image is tagged
    more than once

    [![Documentation](https://img.shields.io/badge/Documentation-Not%20Added%20Yet-inactive)](
    https://post-storm-imagery.readthedocs.io/en/latest/assigner/)
    [![Source](https://img.shields.io/badge/Source-Click%20Me-informational)](
    https://github.com/UNCG-CSE/Poststorm_Imagery/tree/master/src/python/psic/assigner)
    
    **Time:** 75 hours
   
3.  Misc

    I've been working on structuring of the repository and also looking into different strategies to handle the image
    data and the best way to work with it. I've also been tweaking everything, including other scripts to make them
    pretty and working with Nafis to get the dashboard working.
    
    **Time:** *too much*
    

---

### [**Shah Nafis Rafique**](https://github.com/ShahNafisRafique)  

**Hours spent:** A lot 😢, 8 to 13 to 20 per week depending on the week.

[![Documentation](https://img.shields.io/badge/Documentation-Click%20Me-brightgreen)](
https://post-storm-imagery.readthedocs.io/en/latest/dashboard/)

#### What I did

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

Tasks 1-2 took about 2 weeks.  
Tasks 3-7 took the last 3 weeks.

---

### [**John Weber**](https://github.com/JWeb56)  

<!-- Insert tasks here -->
