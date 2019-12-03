# Project Introduction

Research scientists studying the effects of storms on land in the path of travel


## Member Tasks

### [**Rinty Chowdhury**](https://github.com/rintychy)

---

### [**Daniel Foster**](https://github.com/dlfosterbot)

---

### [**Matthew Moretz**](https://github.com/Matmorcat)

---

### [**Shah Nafis Rafique**](https://github.com/ShahNafisRafique)

#### Tagging State History

***Time: 6 hours over the course of a week***

Everytime a user tags an image, the tagging state json file is backed up and renamed to contain the time of backup. What this results in is about 900 json files where each is different from one another because someone tagged an image. So what I did was I went through every 50 or so json files and loaded it into a dataframe and tracked the ratio of incomplete tagged images to the total number of availible tagable images. While this isnt useful, its interesting to see if discrepancies in tagging by people on the same image changes or not.

#### CSV creation

***Time: 2 hours***

Since most of our machine learning models require a CSV of some sorts to contain
the tagging data of the images, I first went ahead and created a script that
given the tagging state json file, will create the CSV from it. First the script
loads the json file into a dataframe, then all `NaN` values are replaced with 0's and all `True` and `False` values are converted over to 1/0.

#### CNN for impact type

***Time: 4 hours in preparing the images, 10 learning on how to CNN***

The first thing I did was try to set up the images. This consisted of first downloading the images, which only took 5 minutes, trying to get python to find the images and copy them over using the `shutil` package. I also foolily tried to hand create my own test/training sets before learning that sklearn has a method to do that.

The CNN part was painful. Earlier in October I had gone to the All Things Open 2019 in Raleigh and one of the talks was about using CNN for image classification. However I didnt learn too much from it. I then tried to go look at Keras it self to see if they had any tutorials of its own, which it had [this](https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html). However there where 2 problems, the first being that in this example they where changing the images them self by rotating,sheering,zooming which lead to various artifacts which would not be suitible for this topic. The bigger issue was that the model took forever. I let it ran for 5 minutes and it didnt even finish 1 epoch. I then tried to have TensorFlow use my GPU since I have RTX, but that also failed due to it requiring that I use Visual Studio IDE. I was able to eventually get all the CNN stuff to work, all thats left is to fine tune the settings to maximize accuracy, do some confusion matrix and test.

---

### [**John Weber**](https://github.com/JWeb56)
