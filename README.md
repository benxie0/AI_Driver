# AI_Driver
Neural Net experimentation for TrackMania AI

## V1
V1 was a simple CNN that took in a filtered and scaled image and outputs a label, 0-14, which corresponds to the label of the keys being pressed. The combo consisted of 0 key combos, 1 key combos, and 2 key combos of WASD. This was and introduction to many new python modules, such as opencv, tensorflow/keras, and a few other helper ones. It also served as a review of python, which I don't usually use too much.

Before the data was inputted, The borders of the track were filtered out and then multiplied by the speed. This was mainly because I wanted to see what the opencv module had to offer, but had the added "benifit" of isolating the track from background noise. The faster the car is, the brighter the image. This greyscale image was the input into the neural net. All the images were also flipped (along with the corresponding controls) to prevent bias when turning. This method worked decently, and the car was able to react to the curves and turn, but it wouldn't do so smoothly, or without crashing.

## V2
The major quality of life change in V2 were various optimizations to lessen the memory and storage usage from the dataset. This meant that I could make and use more data points to train the neural net. Also, the image was less filtered, just cropped to be much much smaller. I reasoned that the model could figure that out on its own during training. Another major change was seperating the "gas pedal" and "steering wheel". The images were flipped, like v1, and then inputted into the neural net. This time, I used two seperate models to train these two sets of controls. This method seemed to work much better. It drove through the first few corners flawlessly. However, during the first run, I noticed that the AI was rarely braking. This lead me to look into using class weights. After tweaking the weights, the AI was able to drive unassisted for a decent amount of time before getting stuck. I think overall I'm satisfied with the results considering the hardware limitations I had. I think one big problem I had other than the simplicity of the network was the training data I collected. It was messy as I am not a very good driver to begin with. A lot of the data might have been inconsistant.

### V2 network model

![Model](https://github.com/benxie0/AI_Driver/blob/master/V2/model.png)
