# Project Introduction

<!--Replace this with an introduction of project (2-3 paragraphs)-->

# Member Tasks:

-   [**Rinty Chowdhury**](https://github.com/rintychy)  

    I was assigned to do two tasks. First task was to download the post-storm images from the NOAA.gov website. 
    There were some initial challenges in downloading large scale files. This was later resolved with the help of my 
    teammates. Finally, it was completed in two weeks. Second task was to create a script to compress the large size 
    .jpg image file. I have created an script to compress all the .jpg image file recursively. Due to the large file 
    size, it takes longer to upload an image on the UI. Smaller size image will be easily uploadable to the dashboard. 
    This task took me one week to finish it. Currently I am working on improving the code and making it more efficient
    and generic. 
    
-   [**Daniel Foster**](https://github.com/dlfosterbot)  

    <!--Replace this with your task-->

-   [**Matthew Moretz**](https://github.com/Matmorcat)  

    <!--Replace this with your task-->
    
-   [**Shah Nafis Rafique**](https://github.com/ShahNafisRafique)  

    <!--Replace this with your task-->
    
-   [**John Weber**](https://github.com/JWeb56)  

    My primary task for the data collection portion of our project was to help download the image archives. Given the hundreds of GBs of data and download speeds capped at around 2-3 MiB/s, and that connections to the NOAA site generally timed out after a few hours, this meant near constant downloading and process monitoring for over a week. In addition to this, I was in charge of researching external tools for tagging images. I found one which was particularly promising, but it didn't seem to allow for the sheer number of images we're dealing with, and so we ultimately decided to use Shah's UI, which he was developing concurrently as a backup plan. Lastly, most recently I "designed" our simple MySQL database which will store the tagged/labeled image data. I have configured a SQL server instance via Google Cloud, and am working on hosting our application on a GCloud VM so that our application can be run on the web. This involves purchasing VM and MySQL storage instances on the Google Cloud Platform, and installing and configuring all necessary packages such that we can run our application on a VM and have it connected to our SQL server so that as soon as an image is tagged via our UI, that information can be relayed to our database.
    
