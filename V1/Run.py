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
model = tf.keras.models.load_model('saved_models/v1.h5')

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
    print(type(key))
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
        screencap = ((screen/255)*(speed+1)*5)/200

        cv2.imshow("test", screencap)

        screencap = screencap.reshape(-1, 48*2, 64*2, 1)
        prediction = model.predict(screencap)

        i = 0
        index = 0
        biggest = 0.0
        for value in prediction[0]:
            if value > biggest:
                index = i
                biggest = value
            i += 1

        print(prediction[0])
        print(index)

        if (index == 0):
            releasek(W)
            releasek(S)
            releasek(A)
            releasek(S)
        elif (index == 1):
            pressk(W)
            releasek(S)
            releasek(A)
            releasek(S)
        elif (index == 2):
            releasek(W)
            pressk(S)
            releasek(A)
            releasek(D)
        elif (index == 3):
            pressk(W)
            pressk(S)
            releasek(A)
            releasek(D)
        elif (index == 4):
            releasek(W)
            releasek(S)
            pressk(A)
            releasek(D)
        elif (index == 5):
            pressk(W)
            releasek(S)
            pressk(A)
            releasek(D)
        elif (index == 6):
            releasek(W)
            pressk(S)
            pressk(A)
            releasek(D)
        elif (index == 8):
            releasek(W)
            releasek(S)
            releasek(A)
            pressk(D)
        elif (index == 9):
            pressk(W)
            releasek(S)
            releasek(A)
            pressk(D)
        elif (index == 10):
            releasek(W)
            pressk(S)
            releasek(A)
            pressk(D)
        elif (index == 12):
            releasek(W)
            releasek(S)
            pressk(A)
            pressk(D)
        else:
            pressk(W)
            releasek(S)
            releasek(A)
            releasek(D)
