import os
import tensorflow as tf
from tensorflow import keras

import numpy as np
from pynput import keyboard
from pynput.keyboard import Key, Controller

import ctypes
import time
import kbinput


mykeyboard = Controller()

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
    kbinput.PressKey(0x11)

    # print(type(key))
    # # try:
    # mykeyboard.press(key)
    # # except:
    # #     pass

def releasek(key):
    try:
        mykeyboard.release(key)
    except:
        pass


listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

while (1):
    if(flag):
        pressk('w')
        print("w")