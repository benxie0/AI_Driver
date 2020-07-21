# based off https://towardsdatascience.com/reinforcement-learning-w-keras-openai-dqns-1eed3a5338c

import gym
import numpy as np
import random
import keras
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
        self.epsilon_decay = 0.9995
        self.learning_rate = 0.01

        # create 2 models for learning and target to help convergence and eliminate a moving target
        self.model = self.create_model()
        self.target_model = self.create_model()

    # make cnn model for training
    def create_model(self):
        shape = self.env.observation_space.shape
        #print(shape)
        # from v2
        model = keras.Sequential()

        model.add(Conv2D(8, (5,5), input_shape = (68, 128, 1)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2,2)))

        # model.add(Conv2D(8, (3,3)))
        # model.add(Activation('relu'))
        # model.add(MaxPooling2D(pool_size=(2,2)))

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
            else:
                Q_future = max(self.target_model.predict(new_state)[0])
                target[0][action] = reward + Q_future * self.gamma

            print("start fit")
            self.model.fit(state, target, epochs=1, verbose=0)
            print("end fit")

    # every once in a while, set the target
    def target_train(self):
        # get weights from current models
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        # copy over weights
        for i in range(len(target_weights)):
            target_weights[i] = weights[i]
        self.target_model.set_weights(target_weights)

    # perform the action based on epsilon (random)
    def act(self, state):
        # update epsilon
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        # do random action
        if np.random.random() < self.epsilon:
            return self.env.action_space.sample()
        # else predict
        #print('predict')
        return np.argmax(self.model.predict(state))
    
    def save_model(self, fn1, fn2):
        self.model.save(fn1)
        self.target_model.save(fn2)

    def main():
        # inport env
        env =  gym.make('gym_env:trackmania-v1')

        # gamma   = 0.9
        # epsilon = .95

        trials  = 1000
        trial_len = 10000

        dqn_agent = DQN(env=env)
        steps = []

        for trial in range(trials):
            # reset the enviroment
            curr_state = env.reset()
            curr_state = curr_state.reshape(-1, 68, 128, 1)
            # go thru trial
            for step in range(trial_len):
                
                action = dqn_agent.act(curr_state)

                # step and get new stuff
                new_state, reward, done, _ = env.step(action)
                new_state = new_state.reshape(-1, 68, 128, 1)

                # store data into memory
                dqn_agent.remember(curr_state, action, reward, new_state, done)

                dqn_agent.replay()       # internally iterates default (prediction) model
                dqn_agent.target_train() # updates target model
                curr_state = new_state    # update state

                # exit if done
                if done:
                    break
                
            # failed if doesnt complete steps
            if (steps < (trial_len - 10)):
                print("trial failed: trial {}, {} steps".format(trail, steps))
                # periodically save
                if (trial % 10 == 0):
                    dqn_agent.save_model("trial-{}-{}.model".format(trial, steps), "target-{}-{}.model".format(trial, steps))
            else:
                dqn_agent.save_model("trial_success", "target_success")

if __name__ == "__main__":
    DQN.main()