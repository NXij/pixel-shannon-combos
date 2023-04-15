#!/usr/bin/env python
import uecaps_pb2 as uecaps_pb2
import sys
import re
import string

with open(sys.argv[1], mode='rb') as file:
    fileContent = file.read()

server = uecaps_pb2.a()
server.ParseFromString(fileContent)

def bandhandler(band):
    if band > 300:
        band = re.sub("^10+(?!$)", "n", str(band))
    return band

def dlcombohandler(band, dlcc):
    dlcc = dlcc - 1
    if dlcc >= 2:
        dlcc = string.ascii_uppercase[dlcc]
    else:
        dlcc = ""
    band = str(bandhandler(band)) + str(dlcc)
    return band

def ulcombohandler(band, ulcc):
    if ulcc > 0:
        if ulcc > 1:
            ulcc = string.ascii_uppercase[ulcc]
        else:
            ulcc = ""
        band = str(bandhandler(band)) + str(ulcc)
        return band

def comboconstructor(combo):
    dlist, ulist = [], []
    for value2 in combo.c:
        dlist.append(dlcombohandler(value2.band, value2.dlcc))
        if ulcombohandler(value2.band, value2.ulcc) != None:
            ulist.append(ulcombohandler(value2.band, value2.ulcc))
    return dlist, ulist


for value in server.a:
    for value1 in value.b:
        dlc = [''.join([('_' if re.match("n.*",i) else '-')+i for i in comboconstructor(value1)[0]])]
        ulc = [''.join([('_' if re.match("n.*",i) else '-')+i for i in comboconstructor(value1)[1]])]
        #nrc = 
        print(dlc[0][1:] + ',' + ulc[0][1:])
        #print('_'.join(comboconstructor(value1)[0]))
        #print('-'.join(['_'.join(comboconstructor(value1)[0])]))
