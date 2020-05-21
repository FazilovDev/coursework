# %%
from HDF.HDFData import HDFArray
import matplotlib.pyplot as plt
import peakdetect as pkd
import os.path
import math
from Analyzer import *
path = './FilteredData/'


f = FileAnalyzer(path + '2.h5')
time = []
intervals = f.get_intervals()
for interval in intervals:
    time.append(interval.get_characteristics()[1])
plt.plot(time)

#%%
file = FileAnalyzer(path + '5.h5')
intervals = file.get_intervals()
print(intervals)
print('speed  time  accuracy')
for interval in intervals:
    ch = interval.get_characterictics()
    print(ch[0], ch[1], ch[2])
f=None
print(f is not None)

#%%
file1 = FileAnalyzer(path + '5.h5')
peaks = file1.get_max_peaks_fd_channel()
print('count peaks = ', len(peaks[0]))
print('count synchro = ', file1.get_count_synchrostimuls())
print('count_click = ', file1.get_count_click())
file1.plot_fd_channel(0,1000) 
file1.get_history()
#%%
count_files = sum(os.path.isfile(os.path.join(path, f)) for f in os.listdir(path))
print('all files = ', count_files)
good_files = []
for i in range(count_files):
    filename = path + str(i) + '.h5'
    print(filename)
    file = FileAnalyzer(filename)
    if (file.is_good_file()):
        good_files.append(filename)
print('good files = ', len(good_files))

# %%
def get_intervals_from_file(file_analyzer):
    if (type(file_analyzer) is not FileAnalyzer):
        return
    count_intervals = file_analyzer.get_count_synchrostimuls()
    intervals = []
    for i in range(count_intervals):



#%%
f = FileAnalyzer(path + '1.h5')
a=  10
print(type(a) is not FileAnalyzer)

# %%
