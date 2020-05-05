# -*- coding: utf8 -*-

import os, sys, inspect
from copy import deepcopy
import logging
import HDFData 
from nose.tools import nottest
from nose.plugins.attrib import attr



dataTemplate1 = {
        'events' : {'time': 'UInt64', 'code': 'Int32'},
        'ecg': {'time': 'UInt64', 'ecg': 'Int16'},
        'pg': {'time': 'UInt64', 'pg': 'Int16'},
        'eeg': {'time': 'Int64', 'A0_B1': 'Int16','A2_B2': 'Int16','C3_H5': 'Int16'}
        }
        
@attr(group='basic')
def HDFWriter_Test():
    fileName = "testHDFFile1.h5"
    writer = HDFData.HDFArray(fileName, dataTemplate1, openMode = 'w')
    writer.appendTable("eeg", {"time": 151565, "A0_B1": 1, "A2_B2": 2, "C3_H5": 3})
    writer.appendTable("eeg", {"time": 151566, "A0_B1": 10, "A2_B2": 20, "C3_H5": 30})
    writer.appendTable("eeg", {"time": 151567, "A0_B1": 100, "A2_B2": 200, "C3_H5": 300})
    writer.appendTable("eeg", {"time": 151568, "A0_B1": 100, "A2_B2": 200, "C3_H5": 300})
    writer.appendTable("eeg", {"time": 151569, "A0_B1": 100, "A2_B2": 200, "C3_H5": 300})
    writer.appendTable("eeg", {"time": 151570, "A0_B1": 100, "A2_B2": 200, "C3_H5": 300})
    writer.appendTable("eeg", {"time": 151571, "A0_B1": 100, "A2_B2": 200, "C3_H5": 300})
    writer.appendTable("ecg", {"time": 151565, "ecg": 3})
    writer.appendTable("pg", {"time": 151565, "pg": 3})
    writer.appendTable("events", {"time": 151565, "code": 567})
    writer.setMainMetaData({"subject": 1, "subjectName": "sdfsdf", "dateTime": 134512301, "Experiment": "DummyExperiment"})
    writer.close()

    reader = HDFData.HDFArray(fileName, dataTemplate1)
    (columnNames, table) = reader.getChannelTable("eeg")
    print(table)
    assert (len(columnNames) == 4)
    assert (table[0,0] == 151565)
    assert (table[0,3] == 3)
    assert (table[2,2] == 200)

    row = reader.getChannelRow("eeg", 0)
    assert(row["time"] == 151565)

    rows = reader.getChannelWithTimeSpan("eeg", 151566, 151567)
    assert(len(rows) == 2)
    assert(rows[0]["time"] == 151566)
    assert(rows[1]["time"] == 151567)

    assert(reader.getMainMetaData("subject") == 1)
    assert(reader.getMainMetaData("Experiment") == "DummyExperiment")

    reader.close()
    
    #fileName = "HDF/testHDFFile1.h5"
    #writer = HDFData.HDFArray(fileName, {'events' : {'time': 'UInt64', 'code': 'Int32'}}, openMode = 'w')
    #writer.close()
    
if __name__ == "__main__":
    HDFWriter_Test()