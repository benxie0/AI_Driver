from pynput import keyboard
import numpy as np

#keypress array
keys = np.zeros(4)

#### Keylogger functions
def on_press(key):
    try:
        if (key.char == 'w'):
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

#start nonblocking listener            
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

while(1):
    #binary to decimal (record keystrokes 0-15)
    keycode = keys[0]*1 + keys[1]*2 + keys[2]*4 + keys[3]*8
    print(keycode)
