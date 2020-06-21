# TensorFlow and tf.keras
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D, Softmax

import numpy as np
import cv2

def translatekeys(a,b):
    temp = a*2+b
    if temp < 3:
        return a*2+b
    else:
        return 0

def getkeys(keycode):
    i = [0,0,0,0]
    if (keycode&1):
        i[0] = 1
    if (keycode&2):
        i[1] = 1
    if (keycode&4):
        i[2] = 1
    if (keycode&8):
        i[3] = 1
    return(i)


datalist = []

data = np.load('inputdata1.npy', allow_pickle=True)
#print(data[-1])
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

# data = np.load('inputdata6.npy', allow_pickle=True)
# tempdatalist = data.tolist()
# datalist = tempdatalist + datalist

# data = np.load('inputdata7.npy', allow_pickle=True)
# tempdatalist = data.tolist()
# datalist = tempdatalist + datalist

# data = np.load('inputdata8.npy', allow_pickle=True)
# tempdatalist = data.tolist()
# datalist = tempdatalist + datalist

tempdatalist = []

X = []
y_throttle = []
y_turn = []
i = 0

for screen, speed, keycode in datalist:
    #print(datalist[1])
    keys = getkeys(keycode)

    # if(keys[3] == 1): 
    #     print(keys[3])

    X.append(((screen/255)*(speed+1)/40))
    y_throttle.append(translatekeys(keys[0], keys[1]))
    y_turn.append(translatekeys(keys[2], keys[3]))

    #flip images+labels to get rid of bias
    X.append(cv2.flip(((screen/255)*(speed+1)/40), 1))
    y_throttle.append(translatekeys(keys[0], keys[1]))
    y_turn.append(translatekeys(keys[3], keys[2]))

datalist = []

X = np.array(X).reshape(-1, 68, 128, 1)
y_throttle = np.array(y_throttle, dtype=np.uint8)
y_turn = np.array(y_turn, dtype=np.uint8)
#print(X)
#print(shape(X))
#print(y)
#print(shape(X))

#print(y_throttle)

# cv2.imshow("test", X[255])
# cv2.waitKey(1000)

## Model for throttle

model_throttle = keras.Sequential()

model_throttle.add(Conv2D(8, (5,5), input_shape = X.shape[1:]))
model_throttle.add(Activation('relu'))
model_throttle.add(MaxPooling2D(pool_size = (2,2)))

model_throttle.add(Conv2D(8, (5,5)))
model_throttle.add(Activation('relu'))
model_throttle.add(MaxPooling2D(pool_size = (2,2)))

model_throttle.add(Flatten())

model_throttle.add(Dense(64))
model_throttle.add(Dropout(.4))
model_throttle.add(Activation('relu'))

model_throttle.add(Dense(32))
model_throttle.add(Activation('relu'))

model_throttle.add(Dense(3))

# compile model
model_throttle.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model_throttle.summary()

#train and save model
model_throttle.fit(X, y_throttle, epochs=4, validation_split=.1)
probability_model_throttle = tf.keras.Sequential([model_throttle, tf.keras.layers.Softmax()])
probability_model_throttle.save('saved_models/throttle.h5')

## Model for turning

model_turn = keras.Sequential()

model_turn.add(Conv2D(8, (5,5), input_shape = X.shape[1:]))
model_turn.add(Activation('relu'))
model_turn.add(MaxPooling2D(pool_size = (2,2)))

model_turn.add(Conv2D(8, (5,5)))
model_turn.add(Activation('relu'))
model_turn.add(MaxPooling2D(pool_size = (2,2)))

model_turn.add(Flatten())

model_turn.add(Dense(64))
model_turn.add(Dropout(.4))
model_turn.add(Activation('relu'))

model_throttle.add(Dense(32))
model_throttle.add(Activation('relu'))

model_turn.add(Dense(3))

# compile model
model_turn.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model_turn.summary()

#train and save model
model_turn.fit(X, y_turn, epochs=6, validation_split=.1)
probability_model_turn = tf.keras.Sequential([model_turn, tf.keras.layers.Softmax()])
probability_model_turn.save('saved_models/turn.h5')