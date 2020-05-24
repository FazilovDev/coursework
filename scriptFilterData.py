# -*- coding: utf8 -*-
# %%
"""
Этот скрипт копирует из папки config.settings.paths.raw в filtered
те файлы, в которых есть все необходимые таблицы
'EEG', 'TRACK_MARKERS', 'ECG', 'FD', 'PNVM'
"""
from HDF.HDFData import HDFArray

from config import settings
path = settings["paths"]["raw"]
filteredPath = settings["paths"]["filtered"]

# опытным путем пришел к выводу, что данных номеров файлов нет среди данных
ban_files = [366, 269, 345, 344, 326, 325]
#for i in range(245, 368):
#    if (i not in ban_files):
#        print("id_files: ", i, "\nkeys: ", HDFArray("RawData/"+str(i) + '.h5').ListChannels().keys())


# %%
true_keys = ['EEG', 'TRACK_MARKERS', 'ECG', 'FD', 'PNVM']
all_files = 368 - 245 - len(ban_files)
good_files = 0
files = []
for i in range(245, 368):
    if (i not in ban_files):
        list_keys = HDFArray(path + str(i) + '.h5').ListChannels().keys()
        k = 0
        for key in true_keys:
            if (key not in list_keys):
                break
            else:
                k+=1
        if (k == len(true_keys)):
            files.append(str(i)+".h5")
            good_files += 1
            print('file good of ', i, '.h5')
print('all files = ', all_files)
print("all good files = ", good_files)
            

# %%
import shutil
for i in range(good_files):
    shutil.copy2(path + files[i], filteredPath+str(i)+'.h5', follow_symlinks=True)
    print('copy good')

