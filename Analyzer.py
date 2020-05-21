import peakdetect as pkd
from HDF.HDFData import HDFArray
import matplotlib.pyplot as plt
import math
import numpy as np
import csv

PATH = 'ds'

class IntervalExperiment:
    def __init__(self,obj_pos, eeg, ecg, pnvm, fd, track):
        self.eeg = eeg
        self.ecg = ecg
        self.pnvm = pnvm
        self.fd = fd
        self.track = track
        self.size_interval = len(fd)
        if (self.size_interval < 10):
            self.size_interval = 1e10
        characteristics = self.__init_characteristics(obj_pos)
        self.reaction_speed = characteristics[0]
        self.reaction_time = characteristics[1]
        self.move_speed = characteristics[2]
        self.move_time = characteristics[3]
        self.accuracy_click = characteristics[4]
    
    def __distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0])*(point1[0] - point2[0]) + (point1[1] - point2[1])*(point1[1] - point2[1]))
    
    def __init_characteristics(self, object_pos):
        if (len(self.track) < 2):
            print('ERROR len track = ', len(self.track),' len interval = ', self.size_interval)
            return [0,0,0,0,0]
        reaction_time = None
        reaction_speed = None
        move_time = None
        move_speed = None
        accuracy_click = None
        delta_px = 5
        click = False
        move = False
        start_signal = self.track[1]
        click_pos = []
        for i in range(len(self.track)):
            if(self.track[i][1] == 50):
                d = self.__distance([self.track[i][2], self.track[i][3]],[start_signal[2],start_signal[3]])
                if (d >= delta_px and reaction_time is None):
                    reaction_time = self.track[i][0] - start_signal[0]
                    d = self.__distance([self.track[i][2],self.track[i][3]],[start_signal[2],start_signal[3]])
                    reaction_speed = d / (self.track[i][0] - start_signal[0])
            elif (self.track[i][1] == 2 and not click):
                click_pos.append(self.track[i][2])
                click_pos.append(self.track[i][3])
                d = self.__distance(click_pos,[start_signal[2],start_signal[3]])
                move_speed = d / (self.track[i][0] - start_signal[0])
                d = self.__distance(click_pos, object_pos)
                accuracy_click = 1 - d / delta_px / delta_px
                move_time = self.track[i][0] - start_signal[0]
                click = True
        if (not click):
            click_pos.append(self.track[self.size_interval-1][2])
            click_pos.append(self.track[self.size_interval-1][3])
            d = self.__distance(click_pos,[start_signal[2],start_signal[3]])
            move_speed = d / (self.track[i][0] - start_signal[0])
            d = self.__distance(click_pos, object_pos)
            accuracy_click = 1 - d / delta_px / delta_px
            move_time = self.track[i][0] - start_signal[0]           
        if (accuracy_click is None):
            accuracy_click = 0
        if (reaction_speed is None and not click):
            reaction_speed = 0
        return [reaction_speed, reaction_time, move_speed, move_time, accuracy_click]
    
    def get_characteristics(self):
        return [self.reaction_speed, self.reaction_time, self.move_speed, self.move_time, self.accuracy_click]

    def get_length(self):
        return self.size_interval
    
    def trim(self, a, b):
        self.eeg = self.eeg[a:b]
        self.ecg = self.ecg[a:b]
        self.pnvm = self.pnvm[a:b]
        self.fd = self.fd[a:b]
        self.track = self.track[a:b]
    
    def save_to_csv(self, filename):
        with open(filename, "w", newline='') as out_file:
            fieldnames = ['Fp1', 'Fpz', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'T3', 'C3', 'Cz', 'C4', 'T4', 'T5',
             'P3', 'Pz', 'P4', 'T6', 'O1', 'Oz', 'O2', 'ecg', 'pnvm', 'fd']
            writer = csv.DictWriter(out_file, delimiter=';', fieldnames=fieldnames)
            writer.writeheader()
            data = np.hstack((self.eeg, np.atleast_2d(self.ecg)))
            data = np.hstack((data, np.atleast_2d(self.pnvm)))
            data = list(np.hstack((data, np.atleast_2d(self.fd))))
            for row in data:
                writer.writerow(row)

# 'Fp1', 'Fpz', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'T3', 'C3', 'Cz', 'C4', 'T4', 'T5', 'P3', 'Pz', 'P4', 'T6', 'O1', 'Oz', 'O2'
# 'ecg'
# 'pnvm'
# 'fd'
class FileAnalyzer:
    def __init__(self, filename):
        self.file = HDFArray(filename)
        self.eeg = self.file.getChannelTable('EEG')[1]
        self.ecg = self.file.getChannelTable('ECG')[1]
        self.fd = self.file.getChannelTable('FD')[1]
        self.pnvm = self.file.getChannelTable('PNVM')[1]
        self.track = self.file.getChannelTable('TRACK_MARKERS')[1]
        self.count_stimuls = 0
        self.count_click = 0
        for i in range(len(self.track)):
            if (self.track[i][1] == 16000):
                self.count_stimuls += 1
            elif (self.track[i][1] == 2):
                self.count_click += 1
        xy = self.__eval_max_peaks_fd_channel()
        self.x_fd_peaks = xy[0]
        self.y_fd_peaks = xy[1]
        self.intervals = []
        self.__eval_intervals()
        self.file.close()

    def __eval_max_peaks_fd_channel(self):
        count_diff_peaks = 2
        _max, _min = pkd.peakdetect(self.fd, None, 50, 50)
        xm = [p[0] for p in _max]
        ym = [p[1] for p in _max]
        if (abs(self.count_stimuls - len(xm)) > count_diff_peaks):
            return xm, ym, 1
        else:
            diff = abs(len(xm) - self.count_stimuls)
            if (len(xm) > self.count_stimuls):
                xm = xm[:-diff]
                ym = ym[:-diff]
            elif (len(xm) < self.count_stimuls):
                self.count_stimuls -= diff
        return [xm, ym]

    def get_max_peaks_fd_channel(self):
        return [self.x_fd_peaks, self.y_fd_peaks]

    def plot_fd_channel(self, a = None, b = None):
        if (a is None or b is None):
            plt.plot(self.fd)
            plt.show()
        else:
            plt.plot(range(a,b), self.fd[a:b])
            plt.show()

    def get_count_synchrostimuls(self):
        return self.count_stimuls

    def get_count_click(self):
        return self.count_click

    def is_good_file(self):
        if (self.count_stimuls != len(self.x_fd_peaks)):
            return False
        return True
    
    def get_data_channels(self):
        return [self.eeg, self.ecg, self.pnvm, self.fd]

    def get_history(self):
        for i in self.track:
            if (i[1] == 16000):
                print('start')
            elif (i[1] - i[1]%10 == 1000):
                print('pos_obj = ', i[2], i[3])
            elif (i[1] == 2):
                print('click')
            elif (i[1] == 0):
                print('clear and stop')
                print('clear_obj = ', i[2], i[3])

    def __get_interval(self, a, b):
        obj_pos = [self.track[a][2],self.track[a][3]]
        a = a + 1
        int_eeg = self.eeg[a:b]
        int_ecg = self.ecg[a:b]
        int_pnvm = self.pnvm[a:b]
        int_fd = self.fd[a:b]
        int_track = self.track[a:b]
        return IntervalExperiment(obj_pos,int_eeg, int_ecg,int_pnvm, int_fd, int_track)

    def __eval_intervals(self):
        start_stimul = None
        end_stimul = None
        is_true_start = False
        count_stim = self.count_stimuls
        stimuls = []
        for i in range(len(self.track)):
            if (self.track[i][1] == 16000):
                stimuls.append(i)
                count_stim -= 1
            elif (self.track[i][1] == 2 and count_stim == 0):
                stimuls.append(i)
        for i in range(1, len(stimuls)-1):
            interval = self.__get_interval(stimuls[i]-1, stimuls[i+1]-1)
            self.intervals.append(interval)

    def get_intervals(self):
        return self.intervals
    
    def get_min_length_intervals(self):
        min_length_interval = self.intervals[0].get_length()
        for interval in self.intervals:
            if (interval.get_length() < min_length_interval):
                min_length_interval = interval.get_length()
        #print('min length interval = ', min_length_interval)
        return min_length_interval

    def trim_intervals_and_save(self, id_begin_interval, min_length_interval):
        _id = id_begin_interval
        for interval in self.intervals:
            interval.trim(0, min_length_interval)
            filename = PATH + str(_id) +'.csv'
            _id += 1
            interval.save_to_csv(filename)

