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

I was assigned to do two tasks. First task was to download the post-storm images from the NOAA.gov website.
There were some initial challenges in downloading large scale files. This was later resolved with the help of my
teammates. Finally, it was completed in two weeks. Second task was to create a script to compress the large size
.jpg image file. I have created an script to compress all the .jpg image file recursively. Due to the large file
size, it takes longer to upload an image on the UI. Smaller size image will be easily uploadable to the dashboard.
This task took me one week to finish it. Currently I am working on improving the code and making it more efficient
and generic.

---

### [**Daniel Foster**](https://github.com/dlfosterbot)

Downloading the images has been the primary challenge for the group and initially I helped test Matt's download
utility. Once the utility became stable, I began researching the metadata that accompanies the images. I wrote a
script to extract the gps coordinates from each image and build a pandas dataframe. This will be useful because the
annotation phase is focused on the coastal photos and we can use the visualization from the gps metadata to prioritize
which images are served first. I also developed a simple method for iterating through each of the directories and
return a count of the number of images per storm. My short term goal is to cleanup and combine the code for these two
projects, retrieve the metadata for the remaining images, and compile a list of images to prioritize for the annotation
phase. As tagged images are delivered, I'll being work on wrangling and parsing through the new data using the methods
we learn in class.

---

### [**Matthew Moretz**](https://github.com/Matmorcat)

Since the beginning of our project, I have been working to get a download script that could handle downloading
images sequentially, and without a lot of hassle. We learned fairly early on that obtaining the data was infeasible
and required repeatedly starting the download every so often, and doing this for dozens of archives spread across
multiple web-pages. I wrote a very complex command-line script that handles many of the challenges we had
downloading the data, with the help of John and Daniel testing it and reporting back bugs they found. We also
decided that it was out intent to publish our work as an open-source project to a number of places, including
pyOpenSci for use by others who want to build off of it or use our tools, so my second goal was to organize the
repository, make sure the beginnings of documentation and code quality checks were built, and go through the
tedious task of configuring continuous integration to work with our project. This required learning new frameworks
such as code coverage, unit tests in python, and documentation building, as well as testing with virtual machines
to ensure the code can compile (via Tox running flake8 and pytest).

---

### [**Shah Nafis Rafique**](https://github.com/ShahNafisRafique)

One of the goals that our mentor mentioned was to have a UI to allow researchers that are on the project to help tag the
storm images. Given that my internship was something similar and that over the summer I learned more about Node.js, I
decided to go ahead and start on it. Initially there was no difficulties as I just had to set up a Node server, have it
render the HTML server side and then send it to the client, which was something I had done numerous times before. The
problematic areas where form validation and making sure that the client submits all the required information, error
checking on the Node server itself and figuring out how we could display the image on the HTML page in a timely manner
as currently it takes about 8-10 seconds to fully display one image. For the last issue Rinty decided to make an image
compression script that we could then run whenever the client requests for an image so that we instead send a smaller
image. That’s about it for now, I plan to either help create an interface for the MySQL server, or perhaps get working
on user authentication as we want only trusted users to tag the images.

---

### [**John Weber**](https://github.com/JWeb56)

My primary task for the data collection portion of our project was to help download the image archives. Given the
hundreds of GiBs of data and download speeds capped at around 2-3 MiBs/s, and that connections to the NOAA site
generally timed out after a few hours, this meant near constant downloading and process monitoring for over a week.
In addition to this, I was in charge of researching external tools for tagging images. I found one which was
particularly promising, but it didn't seem to allow for the sheer number of images we're dealing with, and so we
ultimately decided to use Shah's UI, which he was developing concurrently as a backup plan. Lastly, most recently I
"designed" our simple MySQL database which will store the tagged/labeled image data. I have configured a SQL server
instance via Google Cloud, and am working on hosting our application on a GCloud VM so that our application can be
run on the web. This involves purchasing VM and MySQL storage instances on the Google Cloud Platform, and
installing and configuring all necessary packages such that we can run our application on a VM and have it
connected to our SQL server so that as soon as an image is tagged via our UI, that information can be relayed to
our database.
