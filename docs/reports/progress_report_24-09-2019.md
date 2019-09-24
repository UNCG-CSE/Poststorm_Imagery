# Project Introduction

<!--Replace this with an introduction of project (2-3 paragraphs)-->

## Member Tasks

- [**Rinty Chowdhury**](https://github.com/rintychy)  

I was assigned to do two tasks. First task was to download the post-storm images from the NOAA.gov website. 
There were some initial challenges in downloading large scale files. This was later resolved with the help of my 
teammates. Finally, it was completed in two weeks. Second task was to create a script to compress the large size 
.jpg image file. I have created an script to compress all the .jpg image file recursively. Due to the large file 
size, it takes longer to upload an image on the UI. Smaller size image will be easily uploadable to the dashboard. 
This task took me one week to finish it. Currently I am working on improving the code and making it more efficient
and generic. 

- [**Daniel Foster**](https://github.com/dlfosterbot)  

<!--Replace this with your task-->

- [**Matthew Moretz**](https://github.com/Matmorcat)  

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

- [**Shah Nafis Rafique**](https://github.com/ShahNafisRafique)  

One of the goals that our mentor mentioned was to have a UI to allow researchers that are on the project to help tag the
storm images. Given that my internship was something similar and that over the summer I learned about Node.js went ahead
and assigned this task to my self, with ofcourse telling the other members and our mentors. My goals with the Dashboard
where to have it rendered server side to minimize API calls from the client, have it look nice and use as much
JavaScript as possible for both front end and back end to keep the code and code principles uniform. The tools I used
where React.js for the development of the UI since React allows me to build the page in components, Material-UI which is
a React implimentation of Googles Matieral Design principles. Next.js which is a site generator framework that uses
React and also allows the HTML pages to be rendered server side, Node.js for serving the HTML page and handling backend
related task such has hosting images on a URL, handling the clients responses and interacting with the database. Now
ofcourse there where issues. The first was error handling for the Node server such as invalid URL's or what if the
server could not fetch the initial data to populate the page. The next issue was a design issue, how can I make the
webpage look nice and form validation which is quite hard with React. The final issue, which I have yet to solve now, is
how can I make my code modular. Right now most for code for the website is in one or two JSX files which isnt very
modular and our mentor would like the code to be useable for future project,so making the code modular helps. After I
solve these issues my next short term goals are to error check client input, error check with the database and add user
authentication with Passport.js because we dont want anyone to be able to tag images, we wnat trusted individuals to tag
images. My long term goal is to help with John and figure out how we can start using the full data set, instead of a
small test amount of images like we do now.

- [**John Weber**](https://github.com/JWeb56)  

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
