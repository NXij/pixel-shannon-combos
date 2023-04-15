#!/usr/bin/env python
import uecaps_pb2 as uecaps_pb2
import sys
import re
import string

# Load .binarypb file given as an argument
with open(sys.argv[1], mode='rb') as file:
    fileContent = file.read()

server = uecaps_pb2.a()
server.ParseFromString(fileContent)

# While decompiling the protobuf, the NR band get a leading group of numbers in the form of "100"
# So for example the band n78 looks like "10078"
# LTE bands do not have these leading numbers
# Here we exclude LTE bands and assign an "n" infront of the NR band
def bandhandler(band):
    if band > 300:
        band = re.sub("^10+(?!$)", "n", str(band))
    return band

# Attach the carrier count to the band number as an alphabetic letter
def dlcombohandler(band, dlcc):
    dlcc = dlcc - 1
    if dlcc >= 2:
        dlcc = string.ascii_uppercase[dlcc]
    else:
        dlcc = ""
    band = str(bandhandler(band)) + str(dlcc)
    return band

# The band is not used for uplink if the carrier count is 0
# Attach the carrier count to the band number as an alphabetic letter
def ulcombohandler(band, ulcc):
    if ulcc > 0:
        if ulcc > 1:
            ulcc = string.ascii_uppercase[ulcc]
        else:
            ulcc = ""
        band = str(bandhandler(band)) + str(ulcc)
        return band

# Construct a list for both downlink and uplink combos
def comboconstructor(combo):
    dlist, ulist = [], []
    for value2 in combo.c:
        dlist.append(dlcombohandler(value2.band, value2.dlcc))
        if ulcombohandler(value2.band, value2.ulcc) != None:
            ulist.append(ulcombohandler(value2.band, value2.ulcc))
    return dlist, ulist

# Here I formated the output as a series of strings in the format that is usually found online (cacombos.com etc)
for value in server.a:
    for value1 in value.b:
        dlc = [''.join([('_' if re.match("n.*",i) else '-')+i for i in comboconstructor(value1)[0]])]
        ulc = [''.join([('_' if re.match("n.*",i) else '-')+i for i in comboconstructor(value1)[1]])]
        print(dlc[0][1:] + ',' + ulc[0][1:])
