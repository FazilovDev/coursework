#%%
import numpy as np
import pandas as pd
import os
from HDF.HDFData import HDFArray
import math

# %%

# Берем первый файл данных
file = HDFArray('dataset/0.h5')
# Достаем таблицу трекера
table_track = file.getChannelTable('TRACK_MARKERS')
# Выделяем маркеры трекера
track_markers_columns = table_track[0]
# Выделяем массивы данных трекера
track_markers_data = table_track[1]

# %%
track_filter = []
for i in range(len(track_markers_data)):
    if (track_markers_data[i][1] == 2):
        track_filter.append(track_markers_data[i])
    elif (i != len(track_markers_data) - 1 and track_markers_data[i][1] == 50 and (track_markers_data[i+1][1] != 50)):
        track_filter.append(track_markers_data[i])
    elif (track_markers_data[i][1] == 0):
        track_filter.append(track_markers_data[i])
    elif (track_markers_data[i][1] == 16000):
        track_filter.append(track_markers_data[i])
    elif (track_markers_data[i][1] - track_markers_data[i][1] % 10 == 1000):
        track_filter.append(track_markers_data[i])
for i in track_filter:
    print(i)
# %%
def distance_to(point1, point2):
    return math.sqrt((point1[0]-point2[0])*(point1[0]-point2[0]) + (point1[1]-point2[1])*(point1[1]-point2[1]))
moving_time = 0
time_start_move = time_end_move = 0
position_click = position_object = []
is_move = False
data_moving = []
for i in range(len(track_filter)):
    if (not is_move and track_filter[i][1] == 16000):
        time_start_move = track_filter[i][0]
        is_move = True
    elif (track_filter[i][1] - track_filter[i][1] % 10 == 1000):
        position_object = (track_filter[i][2], track_filter[i][3])
    elif (is_move and track_filter[i][1] == 2):
        position_click = [track_filter[i][2], track_filter[i][3]]
        time_end_move = track_filter[i][0]
    elif (is_move and track_filter[i][1] == 0):
        is_move = False
        moving_time = time_end_move - time_start_move
        move = [moving_time, distance_to(position_click,position_object)]
        data_moving.append(move)
        moving_time = 0
        time_start_move = time_end_move = 0
        position_click = position_object = []
    elif (is_move and track_filter[i][1] == 0 and position_click == 0):
        is_move = False
        moving_time = 0
        time_start_move = time_end_move = 0
        position_click = position_object = []

# %% 365 591
for i in data_moving:
    print(i)

# %%


# %%
