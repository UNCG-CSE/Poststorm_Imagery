from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
from tensorflow import keras as tf

print(tf.__version__)

# Load the fashion-mnist pre-shuffled train data and test data
(x_train, y_train), (x_test, y_test) = tf.datasets.fashion_mnist.load_data()

print("x_train shape:", x_train.shape, "y_train shape:", y_train.shape)


# Print training set shape - note there are 60,000 training data of image size of 28x28, 60,000 train labels)
print("x_train shape:", x_train.shape, "y_train shape:", y_train.shape)

# Print the number of training and test data-sets
print(x_train.shape[0], 'train set')
print(x_test.shape[0], 'test set')

# Define the text labels
fashion_mnist_labels = ["T-shirt/top",  # index 0
                        "Trouser",      # index 1
                        "Pullover",     # index 2
                        "Dress",        # index 3
                        "Coat",         # index 4
                        "Sandal",       # index 5
                        "Shirt",        # index 6
                        "Sneaker",      # index 7
                        "Bag",          # index 8
                        "Ankle boot"]   # index 9

# Image index, you can pick any number between 0 and 59,999
img_index = 10
# y_train contains the labels, ranging from 0 to 9
label_index = y_train[img_index]
# Print the label, for example 2 Pullover
print ("y = " + str(label_index) + " " +(fashion_mnist_labels[label_index]))
# # Show one of the images from the training dataset
plt.imshow(x_train[img_index])

x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255

print("Number of train data - " + str(len(x_train)))
print("Number of test data - " + str(len(x_test)))


# Further break training data into train / validation sets
# (put 5000 into validation set and keep remaining 55,000 for train)
(x_train, x_valid) = x_train[5000:], x_train[:5000]
(y_train, y_valid) = y_train[5000:], y_train[:5000]

# Reshape input data from (28, 28) to (28, 28, 1)
w, h = 28, 28
x_train = x_train.reshape(x_train.shape[0], w, h, 1)
x_valid = x_valid.reshape(x_valid.shape[0], w, h, 1)
x_test = x_test.reshape(x_test.shape[0], w, h, 1)

# One-hot encode the labels
y_train = tf.utils.to_categorical(y_train, 10)
y_valid = tf.utils.to_categorical(y_valid, 10)
y_test = tf.utils.to_categorical(y_test, 10)

# Print training set shape
print("x_train shape:", x_train.shape, "y_train shape:", y_train.shape)

# Print the number of training, validation, and test data-sets
print(x_train.shape[0], 'train set')
print(x_valid.shape[0], 'validation set')
print(x_test.shape[0], 'test set')


model = tf.Sequential()

# CONV 1 64 3x3 filters at stride 1, pad 1
model.add(tf.layers.Conv2D(filters=64, kernel_size=3, strides=1, padding='same',
                           activation='relu', input_shape=(28, 28, 1)))

# BN 1
model.add(tf.layers.BatchNormalization())

# MAX POOL 1
model.add(tf.layers.MaxPooling2D(pool_size=2))
model.add(tf.layers.Dropout(0.5))

# CONV 2
model.add(tf.layers.Conv2D(filters=64, kernel_size=3, strides=1, padding='same', activation='relu'))

# BN 2
model.add(tf.layers.BatchNormalization())

# MAX POOL 2
model.add(tf.layers.MaxPooling2D(pool_size=2))
model.add(tf.layers.Dropout(0.5))

# CONV 3
model.add(tf.layers.Conv2D(filters=64, kernel_size=3, strides=1, padding='same', activation='relu'))

# BN 3
model.add(tf.layers.BatchNormalization())

# MAX POOL 3
model.add(tf.layers.MaxPooling2D(pool_size=2))
model.add(tf.layers.Dropout(0.5))

model.add(tf.layers.Flatten())
model.add(tf.layers.Dense(256, activation='relu'))
model.add(tf.layers.Dropout(0.5))
model.add(tf.layers.Dense(10, activation='softmax'))

# Take a look at the model summary
model.summary()


# Compile the model
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])


# Train the model
model.fit(x_train,
          y_train,
          batch_size=64,
          # Change to 20 epochs
          epochs=20,
          validation_data=(x_valid, y_valid))


# Test Accuracy
# Evaluate the model on test set
score = model.evaluate(x_test, y_test, verbose=0)

# Print test accuracy
print('\n', 'Test accuracy:', score[1])


# Visualize prediction
y_hat = model.predict(x_test)

# Plot a random sample of 10 test images, their predicted labels and ground truth
figure = plt.figure(figsize=(20, 8))
for i, index in enumerate(np.random.choice(x_test.shape[0], size=15, replace=False)):
    ax = figure.add_subplot(3, 5, i + 1, xticks=[], yticks=[])
    # Display each image
    ax.imshow(np.squeeze(x_test[index]))
    predict_index = int(np.argmax(y_hat[index]))
    true_index = int(np.argmax(y_test[index]))
    # Set the title for each image
    ax.set_title("{} ({})".format(fashion_mnist_labels[predict_index],
                                  fashion_mnist_labels[true_index]),
                 color=("green" if predict_index == true_index else "red"))
