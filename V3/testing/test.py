import gym
env =  gym.make('gym_env:trackmania-v1')

done = False

obs, reward, done, empty = env.step(8)

a = [.1,.2,.3,.4,.5]
a[0][3] = 5

print (a)
# while(not done):
#     obs, reward, done, empty = env.step(8)
#     print(reward)
#     if (done == True):
#         print("done")
#     env.render()
#     #print("f")