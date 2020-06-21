from PIL import ImageGrab
import numpy as np
import cv2

def capture_screen():
    frame = ImageGrab.grab(bbox=(0,150,640,510)) #bbox specifies specific region (bbox= x,y,width,height)
    frame_np = np.array(frame)

    dim = (640, 480)
    #dim = (80, 60)
    # resize image
    resized_blur = cv2.resize(frame_np, dim, interpolation = cv2.INTER_NEAREST)
    #Blur Image/Mask
    #kernel = np.array([[1, 1], [1,1]])/4
    #resized_blur = cv2.filter2D(frame_resized,-1,kernel)

    frame_HSV = cv2.cvtColor(resized_blur, cv2.COLOR_BGR2HSV)
    frame_BW = frame_HSV[:,:,0]

    mask = cv2.inRange(frame_BW, 51, 54)
    masked = cv2.bitwise_and(resized_blur,resized_blur,mask = mask)

    return masked

while(True):
    cv2.imshow("test", capture_screen())
    cv2.waitKey(20)
cv2.destroyAllWindows()