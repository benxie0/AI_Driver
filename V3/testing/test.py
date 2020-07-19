import gym
env =  gym.make('gym_env:trackmania-v1')

done = False
while(not done):
    obs, reward, done, empty = env.step(8)
    print(reward)
    if (done == True):
        print("done")
    env.render()
    #print("f")