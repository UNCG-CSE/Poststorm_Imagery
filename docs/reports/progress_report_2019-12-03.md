# Project Introduction

Research scientists studying the effects of storms on land in the path of travel


## Member Tasks

### [**Rinty Chowdhury**](https://github.com/rintychy)

#### Research with the tagged data

***Time: 2 days***

I had to read the prof lecture materials and resources given by prof a lot to figure out how the unsupervised
clustering can be used within given data. I also had to use online help to understand the concept of the KMeans modeling
and how can I implement it within my own data. Every time I was trying to use it in my data, it was not working. It took
a long time for me to figure out how it works with my data.

#### KMeans Model

***Time: 8 hours***

Doing the actual unsupervised clustering plotting and modeling took whole day. First, I apply the KMeans model into my
data and plot the data into a cluster to see how it looks. I tried manipulating the axis and data to see which way it
fits the model best. When I was happy with the clustering data, then I split the data for testing and training. Then I
did the accuracy test and it came up to be 88% accurate which was quite good.

---

### [**Daniel Foster**](https://github.com/dlfosterbot)

***Time: 6 hours***

Used KNN model to predict shoreline versus inland images using blue and green pixel values as features. Resulted in
100% accuracy due to correlation.

---

### [**Matthew Moretz**](https://github.com/Matmorcat)

In order to classify whether the data is wash-over or not, I made a very basic SVM model that could reach about an 82%
accuracy using images compressed to 5% of their original size and converted to grayscale.

### Compression of Feature Space

***Time: 10 hours***

One of the problems I encountered was that the dimensionality was too high to load all 250 images into memory at a time.
I tried multiple different sizes, expanded the amount of heap space of my IDE to 8 GB, and made sure not to use
notebooks in order to reduce memory and CPU overhead. I tried multiple forms of compression to see what would yield the
smallest set of features, while retaining as much information as possible from the original images. 15% compression w/
anti-aliasing was what we used for the dashboard, and it was still too large (almost 1080p resolution). I chose to
compress the images down to 5% (516 x 388) of the original size using nearest neighbor scaling and converted the images
to grayscale, which yielded a much smaller set of features (200,208 features) and still retained a large portion of the
data. It took a fair bit of time to compress all the images and load them into a single DatFrame. There are other
libraries that load data in chunk-wise, but this was a simple test of SVM and dimensionality reduction.

### Testing PCA & Possible Further Reduction

***Time: 2 hours***

Along with the previously mentioned compression, I also performed a principal component analysis to get some insight
and visualize the kind of the data I was working with. From the component analysis, I found that fewer than about
70 principal components (using the 5% compressed, grayscale images) resulted in a 25% loss of variance (See [Figure 1]),
suggesting that the data cannot be split into a small amount of features to reduce feature-space. I also plotted the
data points of a PCA with 2 components and found that while the different classes (wash-over and no wash-over) did
cluster together, there was still too much overlap for there to be an obvious small data solution (See [Figure 2]).
I decided to work with the original grayscale 5% compressed images as the training time was still reasonable to compute.

### Modeling and K-Fold Cross-Validation

***Time: 2 hours***

For the modeling portion, I used a cross-validation approach to help reduce the chance of over-fitting, and tried
many different parameters to try and find what might yield the best results. I found that C did not have a large effect
in the few trials I ran and that the main factor of how accurate the model could get was as a result of the kernel used.
A linear kernel performed better than rbf and polynomial kernels, though only achieving about an 82% accuracy.

For a listing of some of the results and their corresponding parameters, see [SVM Models].


# Most Notable Misc Changes

***Time: Over 100 hours***

- Replace PyUp bot with Dependabot as PyUp bot was misbehaving
- Redid the catalogs to store more filesystem agnostic data and implement checksums, as the data is now provided in repo
- Implemented methods to stack multiple catalogs for statistical analysis over multiple storms
- Updated cataloging documentation
- Added support for almost all edge-cases and storms currently available from NOAA
- Added functionality to download, extract, and manipulate .zip files the same as .tar
- Got the dashboard setup on a VM and production ready with Shah
- Added functionality to assign image tags in batches to increase performance & reduce calls to assigner API
- Initial preparations for distribution of collection portion of project

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

However, there where 2 problems, the first being that in this example they where changing the images them self by
rotating, sheering, zooming which lead to various artifacts which would not be suitable for this topic. The bigger issue
was that the model took forever. I let it ran for 5 minutes and it didnt even finish 1 epoch. I then tried to have
TensorFlow use my GPU since I have RTX, but that also failed due to it requiring that I use Visual Studio IDE. I was
able to eventually get all the CNN stuff to work, all that's left is to fine tune the settings to maximize accuracy, do
some confusion matrix and test.

---

### [**John Weber**](https://github.com/JWeb56)


[Figure 1]: (https://github.com/UNCG-CSE/Poststorm_Imagery/blob/master/docs/slides/figs/wash_over/explained_variance_pca.png)
[Figure 2]: (https://github.com/UNCG-CSE/Poststorm_Imagery/blob/master/docs/slides/figs/wash_over/n2_pca.png)
[SVM Models]: (https://github.com/UNCG-CSE/Poststorm_Imagery/blob/master/docs/slides/figs/wash_over/svm_models.md)
