# -*- coding: utf8 -*-

from tables import *
import numpy
import time
import sys

def isPython3():
    return sys.version_info >= (3, 0)

class HDFArray:
    # пример dataTemplate:
    # {
    #   'events' : {'time': 'UInt64', 'code': 'Int32'},
    #   'ecg': {'time': 'UInt64', 'value': 'Int16'},
    #   'pg': {'time': 'UInt64', 'value': 'Int16'},
    #   'eeg': {'time': 'UInt64', 'names': (['A0_B1','A2_B2','C3_H5'], 'Int16')}
    # }
    def __init__(self, fileName, dataTemplate={}, openMode='r'):
        self.fileName = fileName
        self.openMode = openMode
        if openMode == "r":
            self.file = open_file(fileName, mode='r')
            self.recordTemplates = {}
            self.tables = {}
            self.dataTemplate = {}
            for group in self.file.walk_groups():
                if group._v_name == "raw_data":
                    self.mainGroup = group
                    break
            for table in self.file.list_nodes(self.mainGroup, classname='Table'):
                self.tables[table.name] = table
                self.recordTemplates[table.name] = {}
                for name in table.colnames:
                    self.recordTemplates[table.name][name] = table.coldtypes[name]
        elif openMode == 'rw':
            self.file = open_file(fileName, mode='a')
            self.recordTemplates = {}
            self.tables = {}
            self.dataTemplate = {}
            for group in self.file.walk_groups():
                if group._v_name == "raw_data":
                    self.mainGroup = group
                    break
            for table in self.file.list_nodes(self.mainGroup, classname='Table'):
                self.tables[table.name] = table
                self.recordTemplates[table.name] = {}
                for name in table.colnames:
                    self.recordTemplates[table.name][name] = table.coldtypes[name]
        elif openMode == 'w':
            self.file = open_file(fileName, mode='w', title="experiment data")
            self.recordTemplates = {}
            self.tables = {}
            self.dataTemplate = dataTemplate
            self.mainGroup = self.file.create_group("/", 'raw_data', 'raw experiment data')
            for tableName in dataTemplate:
                self.recordTemplates[tableName] = self.createRecordDescription(dataTemplate[tableName], tableName)
                print('creating table ', tableName)
                self.tables[tableName] = self.createTable(self.mainGroup, tableName, self.recordTemplates[tableName])
        else:
            raise ArgumentError('open mode could be r, rw or w')

    def createTable(self, group, tableName, recordTemplate):
        table = self.file.create_table(self.mainGroup, tableName, recordTemplate)
        return table

    def addTable(self, tableName, recordTemplate):
        recordDesciption = self.createRecordDescription(recordTemplate, tableName)
        table = self.file.create_table(self.mainGroup, tableName, recordDesciption)
        self.tables[tableName] = table
        return table

    def ListChannels(self):
        result = {}
        for name in self.tables:
            targetTable = self.tables[name]
            columns = targetTable.colnames
            columnList = []
            for c in columns:
                columnList.append((c, str(targetTable.coldtypes[c])))
            result[name] = columnList
        return result

    def GetChannelLength(self, channel):
        targetTable = self.tables[channel]
        return len(targetTable)

    def setMainMetaData(self, data):
        for key, value in data.items():
            self.mainGroup._v_attrs[key] = value

    def getMainMetaData(self, key):
        return self.mainGroup._v_attrs[key]

    def getDataType(self, name, number):
        if name == "UInt32":
            return UInt32Col(pos=number)
        elif name == "Int32":
            return Int32Col(pos=number)
        elif name == "Int64":
            return Int64Col(pos=number)
        elif name == "UInt64":
            return UInt64Col(pos=number)
        elif name == "Float32":
            return Float32Col(pos=number)
        elif name == "Int16":
            return Int16Col(pos=number)
        elif name == "String":
            return StringCol(256, pos=number)
        elif name == "|S256" or name == "|s256":
            return StringCol(256, pos=number)
        else:
            print('unknown type name ', name, ' assuming int32')
            return Int32Col(pos=number)

    def createRecordDescription(self, template, tableName):
        
        # this wrapper is taken from
        # https://docs.python.org/3/howto/sorting.html
        # to port comparator for sorted()
        def cmp_to_key(mycmp):
            'Convert a cmp= function into a key= function'
            class K:
                def __init__(self, obj, *args):
                    self.obj = obj
                def __lt__(self, other):
                    return mycmp(self.obj, other.obj) < 0
                def __gt__(self, other):
                    return mycmp(self.obj, other.obj) > 0
                def __eq__(self, other):
                    return mycmp(self.obj, other.obj) == 0
                def __le__(self, other):
                    return mycmp(self.obj, other.obj) <= 0
                def __ge__(self, other):
                    return mycmp(self.obj, other.obj) >= 0
                def __ne__(self, other):
                    return mycmp(self.obj, other.obj) != 0
            return K

        def CompareColumnNames(x, y):
            if x == y:
                return 0
            if x == "time":
                return -1
            if y == "time":
                return 1
            if x == "code":
                return -1
            if y == "code":
                return 1
            if x < y:
                return -1
            else:
                return 1

        fields = {}
        sortedColumnList = []
        for fieldName in template:
            sortedColumnList.append(fieldName)
        #print('unsorted columns: ', sortedColumnList)
        if isPython3():
            sortedColumnList = sorted(sortedColumnList, key=cmp_to_key(CompareColumnNames))
        else:
            sortedColumnList = sorted(sortedColumnList, cmp=CompareColumnNames)
        #print('sorted columns: ', sortedColumnList)
        columnToNumber = {}
        columnNumber = 1
        for name in sortedColumnList:
            columnToNumber[name] = columnNumber
            columnNumber += 1

        for fieldName in template:
            dataType = self.getDataType(template[fieldName], columnToNumber[fieldName])
            fields[fieldName] = dataType
            print('field ', fieldName, 'has type ', dataType)

        return fields

    def getChannelRecords(self, channelName):
        targetTable = self.tables[channelName]
        data = [x for x in targetTable.iterrows()]
        return data

    def hasChannel(self, channelName):
        return self.tables.has_key(channelName)

    def getChannelColumn(self, channelName, columnName):
        targetTable = self.tables[channelName]
        data = [x[columnName] for x in targetTable.iterrows()]
        return data

    def getChannelRow(self, channelName, index):
        targetTable = self.tables[channelName]
        if len(targetTable) > index:
            return targetTable[index]
        else:
            return None

    def getChannelWithTimeSpan(self, channelName, start, finish):
        targetTable = self.tables[channelName]
        columns = targetTable.colnames
        condition = """(time >= %s) & (time <= %s)""" % (start, finish)
        resultRows = targetTable.where(condition)
        rows = []
        for r in resultRows:
            d = {}
            for n in columns:
                d[n] = r[n]
            rows.append(d)
        return rows

    def getChannelTable(self, channelName, columns=[]):
        targetTable = self.tables[channelName]
        if columns == []:
            columns = targetTable.colnames
        n = targetTable.nrows
        m = len(columns)
        result = numpy.zeros([n, m])
        i = 0
        for x in targetTable.iterrows():
            j = 0
            for name in columns:
                result[i, j] = x[name]
                j += 1
            i += 1
        return (columns, result)

    def appendTable(self, channel, dataToAdd):
        tableRow = self.tables[channel].row
        for key in dataToAdd:
            tableRow[key] = dataToAdd[key]
        tableRow.append()
        self.tables[channel].flush()

    def close(self):
        self.file.close()
