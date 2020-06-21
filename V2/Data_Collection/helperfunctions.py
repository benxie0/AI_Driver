from PIL import ImageGrab
from pynput import keyboard
import numpy as np
import cv2

# def capture_speed():
#     frame = ImageGrab.grab(bbox=(590,486,640,512)) #bbox specifies specific region (bbox= x,y,width,height)
#     frame_np = np.array(frame)
#     frame_BW = cv2.cvtColor(frame_np, cv2.COLOR_BGR2GRAY)
#     out = cv2.inRange(frame_BW, 200, 256)
    
#     kernel = np.array([[1, 1, 1], [1,1,1], [1,1,1]])/9
#     temp = cv2.filter2D(out,-1,kernel)
#     out = cv2.inRange(temp, 50, 256)
    
#     return out

def getspeed():
    frame = ImageGrab.grab(bbox=(590,486,640,512)) #bbox specifies specific region (bbox= x,y,width,height)
    frame_np = np.array(frame)
    frame_BW = cv2.cvtColor(frame_np, cv2.COLOR_BGR2GRAY)
    out = cv2.inRange(frame_BW, 200, 256)
    
    kernel = np.array([[1, 1, 1], [1,1,1], [1,1,1]])/9
    temp = cv2.filter2D(out,-1,kernel)
    input = cv2.inRange(temp, 50, 256)

    d1array = np.zeros(7)
    d2array = np.zeros(7)

# top digit: 1: 11,8   A: 8,3 B: 13,9 C: 13,18 D: 8,21 E: 5,17 F: 5,7 G: 8,12
    if input[2,6] == 255:
        d1array[0] = 1
    if input[8,12] == 255:
        d1array[1] = 1
    if input[17,12] == 255:
        d1array[2] = 1
    if input[20,7] == 255:
        d1array[3] = 1
    if input[16,3] == 255:
        d1array[4] = 1
    if input[6,3] == 255:
        d1array[5] = 1
    if input[11,6] == 255:
        d1array[6] = 1

# second digit: 1: 25,8  A: 23,3 B: 28,8, C:28.17 D: 22,22 E: 19,18 F: 19,8 G: 23,13
    if input[2,21] == 255:
        d2array[0] = 1
    if input[7,27] == 255:
        d2array[1] = 1
    if input[16,27] == 255:
        d2array[2] = 1
    if input[20,22] == 255:
        d2array[3] = 1
    if input[17,18] == 255:
        d2array[4] = 1
    if input[7,18] == 255:
        d2array[5] = 1
    if input[11,22] == 255:
        d2array[6] = 1

    if input[16,9] == 255:
        digit1 = 1
    elif np.all(d1array == [1,1,1,1,1,1,0]):
        digit1 = 0
    elif np.all(d1array == [1,1,0,1,1,0,1]):
        digit1 = 2
    elif np.all(d1array == [1,1,1,1,0,0,1]):
        digit1 = 3
    elif np.all(d1array == [0,1,1,0,0,1,1]):
        digit1 = 4
    elif np.all(d1array == [1,0,1,1,0,1,1]):
        digit1 = 5
    elif np.all(d1array == [1,0,1,1,1,1,1]):
        digit1 = 6
    elif np.all(d1array == [1,1,1,0,0,0,0]):
        digit1 = 7
    elif np.all(d1array == [1,1,1,1,1,1,1]):
        digit1 = 8
    elif np.all(d1array == [1,1,1,1,0,1,1]):
        digit1 = 9
    else: digit1 = 0

    if input[16,23] == 255:
        digit2 = 1
    elif np.all(d2array == [1,1,1,1,1,1,0]):
        digit2 = 0
    elif np.all(d2array == [1,1,0,1,1,0,1]):
        digit2 = 2
    elif np.all(d2array == [1,1,1,1,0,0,1]):
        digit2 = 3
    elif np.all(d2array == [0,1,1,0,0,1,1]):
        digit2 = 4
    elif np.all(d2array == [1,0,1,1,0,1,1]):
        digit2 = 5
    elif np.all(d2array == [1,0,1,1,1,1,1]):
        digit2 = 6
    elif np.all(d2array == [1,1,1,0,0,0,0]):
        digit2 = 7
    elif np.all(d2array == [1,1,1,1,1,1,1]):
        digit2 = 8
    elif np.all(d2array == [1,1,1,1,0,1,1]):
        digit2 = 9
    else: digit2 = 0

    #print(d1array)

    return digit1*10+digit2

def capture_screen():
    frame = ImageGrab.grab(bbox=(0,240,640,460)) #bbox specifies specific region (bbox= x,y,width,height)
    frame_np = np.array(frame, dtype=np.uint8)

    #dim = (640, 480)
    dim = (128, 68)
    #dim = (80, 60)
    # resize image
    resized_blur = cv2.resize(frame_np, dim, interpolation = cv2.INTER_NEAREST)
    #Blur Image/Mask
    #kernel = np.array([[1, 1], [1,1]])/4
    #resized_blur = cv2.filter2D(frame_resized,-1,kernel)

    #frame_HSV = cv2.cvtColor(resized_blur, cv2.COLOR_BGR2RGB)
    frame_BW = resized_blur[:,:,2]

    # mask = cv2.inRange(frame_BW, 45, 60)
    # masked = cv2.bitwise_and(resized_blur,resized_blur,mask = mask)
    
    # return mask and background color
    #return masked

    #return small image
    return frame_BW


####
