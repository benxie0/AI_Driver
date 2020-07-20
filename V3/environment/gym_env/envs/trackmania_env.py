import gym
import gym_env.envs.helperfunctions as helperfunctions

from gym import error, spaces, utils
from gym.utils import seeding

import numpy as np
import time
import cv2


class TrackmaniaEnv(gym.Env):
  metadata = {'render.modes': ['human']}
  def __init__(self):
    """
    Every environment should be derived from gym.Env and at least contain the variables observation_space and action_space 
    specifying the type of possible observations and actions using spaces.Box or spaces.Discrete.

    Example:
    >>> EnvTest = FooEnv()
    >>> EnvTest.observation_space=spaces.Box(low=-1, high=1, shape=(3,4))
    >>> EnvTest.action_space=spaces.Discrete(2)
    """
    """
    action space:
    W, A, S, D, WA, WD, SA, SD, None
    
    obs space:
    Screencap from helperfunctions
    """
    global speed

    speed = [0,0,0,0,0,0]

    self.action_space=spaces.Discrete(9)
    self.observation_space=spaces.Box(np.zeros((68, 128)), np.ones((68, 128)), dtype=np.float)

    time.sleep(3)

  def step(self, action):
    """
    This method is the primary interface between environment and agent.

    Paramters: 
        action: int
                the index of the respective action (if action space is discrete)

    Returns:
        output: (array, float, bool)
                information provided by the environment about its current state:
                (observation, reward, done)
    """
    global speed, obs

    helperfunctions.trans_index(action)
    #print(action)

    speed[0] = helperfunctions.getspeed()
    accel = speed[0] - speed[5]

    # hopefully detect crash
    if (accel<-5 and (speed[2]-speed[4]<-2)):
      done = True
    else:
      done = False
    speed[5] = speed[4]
    speed[4] = speed[3]
    speed[3] = speed[2]
    speed[2] = speed[1]
    speed[1] = speed[0]

    screen = helperfunctions.capture_screen()
    obs = (screen/255)*(speed[0]+1)/40

    # reward (somewhat normalized)
    reward = (speed[0]-10.0)/20.0 #+ accel*5

    return obs, reward, done, {}

  def reset(self):
    """
    This method resets the environment to its initial values.

    Returns:
        observation:    array
                        the initial state of the environment
    """
    helperfunctions.reset()

    time.sleep(3)

    screen = helperfunctions.capture_screen()
    obs = (screen/255)*(speed+1)/40
    
    return obs

  def render(self, mode='human', close=False):
    """
    This methods provides the option to render the environment's behavior to a window 
    which should be readable to the human eye if mode is set to 'human'.
    """

    cv2.imshow("test", obs)
    cv2.waitKey(1)

    #print("a")
    return
