# AI_Driver
Neural Net experimentation for TrackMania AI

## V1
V1 was a simple CNN that took in a filtered and scaled image and outputs a label, 0-14, which corresponds to the label of the keys being pressed. The combo consisted of 0 key combos, 1 key combos, and 2 key combos of WASD. Before the data was inputted, The borders of the track were filtered out and then multiplied by the speed. The faster the car is, the brighter the image. This greyscale image was the input into the neural net. This method worked decently, and the car was able to react to the curves and turn, but it wouldn't do so smoothly, or without crashing.

## V2
The major quality of life change in V2 were various optimizations to lessen the memory and storage usage from the dataset. This meant that I could make and use more data points to train the neural net. Also, the image was less filtered, just cropped to be much much smaller. Another major change was seperating the "gas pedal" and "steering wheel". This time, I used two nets to train these two sets of controls. This method seemed to work much better. It drove through the first few corners flawlessly. However, during the first run, I noticed that the AI was rarely braking. This lead me to look into using class weights. 
