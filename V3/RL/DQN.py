# based off https://towardsdatascience.com/reinforcement-learning-w-keras-openai-dqns-1eed3a5338c

import gym
import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, Activation, MaxPooling2D, Flatten
from keras.optimizers import Adam

from collections import deque

class DQN:
    # set up variables and hyperparams and models and stuff
    def __init__(self, env):
        self.env = env
        # set up memory to train off of
        self.memory = deque(maxlen=2000)

        # hyperparams: gamma = rewards deprecation, epsilon/ep_min/ep_decay = exploration, lr=lr
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.01

        # create 2 models for learning and target to help convergence and eliminate a moving target
        self.model = self.create_model()
        self.target_model = self.create_model()

    # make cnn model for training
    def create_model(self):
        shape = self.env.observation_space.shape

        # from v2
        model = keras.Sequential()

        model.add(Conv2D(8, (5,5), input_shape = shape))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2,2)))

        model.add(Conv2D(8, (3,3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2,2)))

        model.add(Flatten())

        model.add(Dense(32))
        model.add(Activation('relu'))

        model.add(Dense(self.env.action_space.n))

        model.compile(loss="mean_squared_error",
            optimizer=Adam(lr=self.learning_rate))

        return model

    # store data into memory FIFO queue
    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    # replay data from memory for training
    def replay(self):
        # size of randomly chosen training batch, return if memory doesn't have enough data
        batch_size = 32
        if (len(self.memory) < batch_size):
            return

        # get random samples
        samples = random.sample(self.memory, batch_size)

        # train off samples
        for sample in samples:
            state, action, reward, new_state, done = sample
            target = self.target_model.predict(state)

            # get reward (if last sample cant predict future rewards)
            if done:
                target[0][action] = reward