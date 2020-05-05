# %%
from HDF.HDFData import HDFArray
path = "./FilteredData/"
# %%
file = HDFArray(path + '0.h5')
print(file.ListChannels())

# %%

print(len(file.getChannelTable('TRACK_MARKERS')[1]))
print(len(file.getChannelTable('FD')[1]))
# %%
table_track = file.getChannelTable('TRACK_MARKERS')
print(table_track)
print(type(table_track[1]))
track = table_track[1]

# %%
print(len(track[0]))
matrix = track[1]
for i in range(300):
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

print("count = ",count)

# %%
import pandas as pd

data_frame = pd.DataFrame(array_track, columns = table_track[0])
print(data_frame.head())


# %%
for i in range(len(array_track)):
    if (track[i][1] == 0):
        print(array_track[i])
    elif (track[i][1] - track[i][1] % 10 == 1000):
        track_filter.append(array_track[i])
    elif ()

# %%
track_filter = []
flag_move = False
for i in range(len(array_track)):
    if (array_track[i][1] == 2):
        track_filter.append(array_track[i])
        flag_move = True
    elif (i != len(array_track) - 1 and array_track[i][1] == 50 and (array_track[i+1][1] != 50)):
        track_filter.append(array_track[i])
    elif (array_track[i][1] == 0):
        track_filter.append(array_track[i])
    elif (array_track[i][1] == 16000):
        track_filter.append(array_track[i])
    elif (array_track[i][1] - array_track[i][1] % 10 == 1000):
        track_filter.append(array_track[i])

# %%
for i in track_filter:
    print(i)

# %%
print(50 - 50 % 10 == 1000)

# %%
radius = 5
print((287-280) / radius)

# %%
