# %%
from HDF.HDFData import HDFArray
path = "./FilteredData/"

# %%
file = HDFArray(path + '0.h5')
print(file.ListChannels())

# %%
fd = file.getChannelTable('FD')[1]
print(len(fd))
for i in range(1000):
    print(fd[i])
#%%

import matplotlib.pyplot as plt
plt.plot(fd)
# %%

print(len(file.getChannelTable('TRACK_MARKERS')[1]))
print(len(file.getChannelTable('FD')[1]))

# %%
table_track = file.getChannelTable('TRACK_MARKERS')
print(table_track)
print(type(table_track[1]))
track = table_track[1]
eeg = file.getChannelTable('EEG')
print(eeg)
# %%
print(len(track[0]))
matrix = track[1]
for i in range(500):
    print(track[i])

# %%
filtered_track = []
isMove = False
start = 0
stop = 0
time_start = 0
time_stop = 0
count = 0
for i in range(2, len(track)):
    if (track[i][1] == 16000):
        start = i
        filtered_track.append(track[i])
        time_start = track[i][0]
    elif (track[i][1] == 2):
        filtered_track.append(track[i])
        stop = i
        time_stop = track[i][0]
        count += 1
        print("dif = ", stop-start)
        print("time = ", time_stop-time_start)
print(time_stop, time_start)
c = 0

