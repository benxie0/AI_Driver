import time
import helperfunctions
from PIL import ImageGrab
import numpy as np
import cv2
import json
from pynput import keyboard

#keypress array
keys = np.zeros(4, dtype=np.uint8)
captureflag = 0

#### Keylogger functions
def on_press(key):
    global captureflag
    global keys
    try:
        if (key.char == 'e'):
            captureflag = (captureflag+1)%2
        elif (key.char == 'w'):
            keys[0] = 1
        elif (key.char == 's'):
            keys[1] = 1
        elif (key.char == 'a'):
            keys[2] = 1
        elif (key.char == 'd'):
            keys[3] = 1
    except AttributeError:
        pass
def on_release(key):
    try:
        if (key.char == 'w'):
            keys[0] = 0
        elif (key.char == 's'):
            keys[1] = 0
        elif (key.char == 'a'):
            keys[2] = 0
        elif (key.char == 'd'):
            keys[3] = 0
    except AttributeError:
        if key == keyboard.Key.esc:
        # Stop listener
            return False



#code start
samples = 0
training_data = []
oldspeed = 0

#start nonblocking listener            
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

print("idle")

#wait for capture to start
while(captureflag != 1):
    time.sleep(.2)
#infinite while loop
print ("capturing data")

while (captureflag):
    #binary to decimal (record keystrokes 0-15)
    keycode = keys[0]*1 + keys[1]*2 + keys[2]*4 + keys[3]*8

    #get screen capture
    screen = helperfunctions.capture_screen()

    #get speed (probably should test before actual data capture)
    speed = helperfunctions.getspeed()

    # if (speed - oldspeed)*(speed - oldspeed) > 10:
    #     speed = oldspeed
    # oldspeed = speed
    #print(type(screen[1][1]))
    #print(keycode)
    # multiply speed and screen to get final value (embeds speed into screenshot? idk im just guessing here)
    #screencap = ((screen/255)*(speed+1)*5)/200

    #print(screencap)
    cv2.imshow("test", screen)
    cv2.waitKey(1)

    # append to training data
    # training_data.append([screen, speed, keycode])
    
    # only get braking data
    if (keys[1]):
        samples += 1
        training_data.append([screen, speed, keycode])
        print (speed)
    
    time.sleep(.01)
    #print(samples)
    #print(speed)
    # ~50fps

print(samples)
np.save('inputdata.npy', training_data)

data = np.load('inputdata.npy', allow_pickle=True)

print(data[-1])