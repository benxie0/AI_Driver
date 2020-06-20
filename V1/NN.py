# TensorFlow and tf.keras
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D, Softmax

import numpy as np
import cv2

data = np.load('inputdata1.npy', allow_pickle=True)
datalist = data.tolist()

X = []
y = []

for features, labels in datalist:
    X.append(features)
    y.append(labels)

X = np.array(X).reshape(-1, 48*2, 64*2, 1)
y = np.array(y)
#print(X)
#print(shape(X))
print(y)
#print(shape(X))

#cv2.imshow("test", X[1])
#cv2.waitKey(0)

model = keras.Sequential()

model.add(Conv2D(32, (3,3), input_shape = X.shape[1:]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size = (2,2)))

model.add(Conv2D(16, (3,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size = (2,2)))

model.add(Conv2D(16, (3,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size = (2,2)))

model.add(Flatten())

# model.add(Dense(256))
# model.add(Activation('relu'))

model.add(Dense(64))
model.add(Activation('relu'))

model.add(Dense(14))

# compile model
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.summary()

#train model
model.fit(X, y, epochs=2, validation_split=.2)

probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])

probability_model.save('saved_models/V1.h5')
