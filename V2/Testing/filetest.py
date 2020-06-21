import numpy as np

data = np.load('inputdata.npy', allow_pickle=True)

#print(data[-1])

i = [0, 0, 0, 0]
if (6&1):
    i[0] = 1
if (6&2):
    i[1] = 1
if (6&4):
    i[2] = 1
if (6&8):
    i[3] = 1

print(i)