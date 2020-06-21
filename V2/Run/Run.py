import os
import tensorflow as tf
from tensorflow import keras

import numpy as np
from pynput import keyboard
from pynput.keyboard import Key, Controller
import cv2

import helperfunctions
import kbinput
import time

W = 0x11
A = 0x1E
S = 0x1F
D = 0x20

mykeyboard = Controller()
model_throttle = tf.keras.models.load_model('saved_models/throttle.h5')
model_turn = tf.keras.models.load_model('saved_models/turn.h5')

flag = 0

#### Keylogger functions
def on_press(key):
    global flag
    try:
        if (key.char == 'e'):
            print("e pressed")
            flag = (flag+1)%2
    except AttributeError:
        pass
def on_release(key):
    if key == keyboard.Key.esc:
    # Stop listener
        return False

# try keyboard functions
def pressk(key):
    #print(type(key))
    try:
        kbinput.PressKey(key)
    except:
        pass

def releasek(key):
    try:
        kbinput.ReleaseKey(key)
    except:
        pass


listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

while (1):
    if(flag):
        screen = helperfunctions.capture_screen()
        #get speed (probably should test before actual data capture)
        speed = helperfunctions.getspeed()
        screencap = ((screen/255)*(speed+1)/40)

        # cv2.imshow("test", screen)
        # cv2.waitKey(1)

        screencap = screencap.reshape(-1, 68,128, 1)
        prediction_th = model_throttle.predict(screencap)
        prediction_tu = model_turn.predict(screencap)

        print(prediction_th)

        i = 0
        index_th = 0
        biggest_th = 0.0
        index_tu = 0
        biggest_tu = 0.0
        for value_th in prediction_th[0]:
            if value_th > biggest_th:
                index_th = i
                biggest_th = value_th
            if prediction_tu[0][i] > biggest_tu:
                index_tu = i
                biggest_tu = prediction_tu[0][i]
            i += 1

        #print(prediction[0])
        print(index_th)

        if (index_th == 0):
            releasek(W)
            releasek(S)
        elif (index_th == 2):
            pressk(W)
            releasek(S)
        elif (index_th == 1):
            releasek(W)
            pressk(S)
        elif (index_th == 3):
            pressk(W)
            pressk(S)
        else:
            releasek(W)
            releasek(S)

        if (index_tu == 0):
            releasek(A)
            releasek(D)
        elif (index_tu == 2):
            pressk(A)
            releasek(D)
        elif (index_tu == 1):
            releasek(A)
            pressk(D)
        elif (index_tu == 3):
            pressk(A)
            pressk(D)
        else:
            releasek(A)
            releasek(D)

