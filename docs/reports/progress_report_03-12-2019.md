# Project Introduction

Research scientists studying the effects of storms on land in the path of travel


## Member Tasks

### [**Rinty Chowdhury**](https://github.com/rintychy)

#### Research with the tagged data

***Time: 2 days***

I had to read the prof lecture materials and resoureces given by prof a lot to figure out how the unsupervised clustering can be used within given data. I also had to use online help to understand the concept of the KMeans modeling and how can I implement it within my own data. Everytime I was trying to use it in my data, it was not working. It took long time for me to figure out how it works with my data.

#### KMeans Model

***Time: 8 hours***

Doing the actual unsupervised clustering ploting and modeling took whole day. First, I apply the kmeans model into my data and plot the data into a cluster to see how it looks. I tried manupulating the axis and data to see which way it fits the model best. When I was happy with the clustering data, then I split the data for testing and training. Then i did the accuracy test and it came up to be 88% accurate which was quite good.


### [**Daniel Foster**](https://github.com/dlfosterbot)
***Time: 6 hours***

Used KNN model to predict shoreline versus inland images using blue and green pixel values as features. Resulted in 100% accuracy due to correlation.

### [**Matthew Moretz**](https://github.com/Matmorcat)

---

### [**Shah Nafis Rafique**](https://github.com/ShahNafisRafique)

#### Tagging State History

***Time: 6 hours over the course of a week***

Every time a user tags an image, the tagging state json file is backed up and renamed to contain the time of backup.
What this results in is about 900 json files where each is different from one another because someone tagged an image.
So what I did was I went through every 50 or so json files and loaded it into a DataFrame and tracked the ratio of
incomplete tagged images to the total number of available tagable images. While this isn't useful, it's interesting to
see if discrepancies in tagging by people on the same image changes or not.

#### CSV creation

***Time: 2 hours***

Since most of our machine learning models require a CSV of some sorts to contain the tagging data of the images, I first
went ahead and created a script that given the tagging state json file, will create the CSV from it. First the script
loads the json file into a DataFrame, then all `NaN` values are replaced with 0's and all `True` and `False` values are
converted over to 1 and 0 respectively.

#### CNN for impact type

***Time: 4 hours in preparing the images, 10 learning on how to CNN***

The first thing I did was try to set up the images. This consisted of first downloading the images, which only took 5
minutes, trying to get python to find the images and copy them over using the `shutil` package. I also foolishly tried
to hand create my own test/training sets before learning that sci-kit learn has a method to do that.

The CNN part was painful. Earlier in October I had gone to the All Things Open 2019 in Raleigh and one of the talks was
about using CNN for image classification. However I didnt learn too much from it. I then tried to go look at Keras
itself to see if they had any tutorials of its own, which it had
[this](https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html).
However there where 2 problems, the first being that in this example they where changing the images them self by
rotating, sheering, zooming which lead to various artifacts which would not be suitable for this topic. The bigger issue
was that the model took forever. I let it ran for 5 minutes and it didnt even finish 1 epoch. I then tried to have
TensorFlow use my GPU since I have RTX, but that also failed due to it requiring that I use Visual Studio IDE. I was
able to eventually get all the CNN stuff to work, all that's left is to fine tune the settings to maximize accuracy, do
some confusion matrix and test.

---

### [**John Weber**](https://github.com/JWeb56)
