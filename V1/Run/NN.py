# TensorFlow and tf.keras
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D, Softmax

import numpy as np
import cv2

def flipkey(keycode):
        if (keycode == 0):
            return(0)
        elif (keycode == 1):
            return(1)
        elif (keycode == 2):
            return(2)
        elif (keycode == 3):
            return(3)
        elif (keycode == 4):
            return(8)
        elif (keycode == 5):
            return(9)
        elif (keycode == 6):
            return(10)
        elif (keycode == 8):
            return(4)
        elif (keycode == 9):
            return(5)
        elif (keycode == 10):
            return(6)
        elif (keycode == 12):
            return(12)
        else:
            return(0)


datalist = []

data = np.load('inputdata1.npy', allow_pickle=True)
tempdatalist = data.tolist()
datalist = tempdatalist + datalist

data = np.load('inputdata2.npy', allow_pickle=True)
tempdatalist = data.tolist()
datalist = tempdatalist + datalist

data = np.load('inputdata3.npy', allow_pickle=True)
tempdatalist = data.tolist()
datalist = tempdatalist + datalist

data = np.load('inputdata4.npy', allow_pickle=True)
tempdatalist = data.tolist()
datalist = tempdatalist + datalist


#datalist = []
data = np.load('inputdata5.npy', allow_pickle=True)
tempdatalist = data.tolist()
datalist = tempdatalist + datalist

data = np.load('inputdata6.npy', allow_pickle=True)
tempdatalist = data.tolist()
datalist = tempdatalist + datalist

data = np.load('inputdata7.npy', allow_pickle=True)
tempdatalist = data.tolist()
datalist = tempdatalist + datalist

data = np.load('inputdata8.npy', allow_pickle=True)
tempdatalist = data.tolist()
datalist = tempdatalist + datalist


X = []
y = []

for features, labels in datalist:
    X.append(features)
    y.append(labels)

    #flip images+labels to get rid of bias
    X.append(cv2.flip(features, 1))
    y.append(flipkey(labels))

datalist = []

X = np.array(X).reshape(-1, 48*2, 64*2, 1)
y = np.array(y)
#print(X)
#print(shape(X))
print(y)
#print(shape(X))

#cv2.imshow("test", X[1])
#cv2.waitKey(0)

model = keras.Sequential()

model.add(Conv2D(8, (3,3), input_shape = X.shape[1:]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size = (2,2)))

model.add(Conv2D(8, (3,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size = (2,2)))

# model.add(Conv2D(8, (3,3)))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size = (2,2)))

model.add(Flatten())

# model.add(Dense(256))
# model.add(Activation('relu'))

model.add(Dense(64))
model.add(Activation('relu'))

model.add(Dense(4))
model.add(Activation('relu'))

model.add(Dense(14))

# compile model
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.summary()

#train model
model.fit(X, y, epochs=3, validation_split=.05)

probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])

probability_model.save('saved_models/V1.h5')
