#!/usr/bin/env python
import uecaps_pb2 as uecaps_pb2
import sys
import re
import string
import struct

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
        ulcc = ulcc - 1
        if ulcc > 1:
            ulcc = string.ascii_uppercase[ulcc]
        else:
            ulcc = ""
        band = str(bandhandler(band)) + str(ulcc)
        return band

# Handles featuresets
def featuresetcontructor(fs, param):
    a, b, c, d, e = [], [], [], [], []
    for i in fs:
        if i != 0:
            i = i - 1
            if i != None:
                if i >= 27:
                    a.append(1), b.append(100), c.append(None), d.append(None), e.append(None)
                else:
                    if param == 1:
                        a.append(server.abfs[i].layer)
                    else:
                        a.append(server.abfs[i].layer * 2)
                    b.append(server.abfs[i].bw), c.append(server.abfs[i].ba), d.append(server.abfs[i].bb), e.append(server.abfs[i].bc)
            else:
                return None
    return a, b, c, d, e

# Construct lists for both downlink and uplink values
def comboconstructor(combo):
    dlist, ulist, fsdl, fsul, bwdl, bwul, fsadl, fsbdl, fscdl, fsaul, fsbul, fscul = [], [], [], [], [], [], [], [], [], [], [], []
    for value2 in combo.c:
        dlist.append(dlcombohandler(value2.band, value2.dlcc))
        if ulcombohandler(value2.band, value2.ulcc) != None:
            ulist.append(ulcombohandler(value2.band, value2.ulcc))
        if featuresetcontructor(value2.fsdl, 0) != None:
            fsdl.extend(featuresetcontructor(value2.fsdl, 0)[0]), bwdl.extend(featuresetcontructor(value2.fsdl, 0)[1]), fsadl.extend(featuresetcontructor(value2.fsdl, 0)[2])
            fsbdl.extend(featuresetcontructor(value2.fsdl, 0)[3]), fscdl.extend(featuresetcontructor(value2.fsdl, 0)[4])
        if featuresetcontructor(value2.fsul, 1) != None:
            fsul.extend(featuresetcontructor(value2.fsul, 1)[0]), bwul.extend(featuresetcontructor(value2.fsul, 1)[1]), fsaul.extend(featuresetcontructor(value2.fsul, 1)[2])
            fsbul.extend(featuresetcontructor(value2.fsul, 1)[3]), fscul.extend(featuresetcontructor(value2.fsul, 1)[4])
    return dlist, ulist, fsdl, fsul, bwdl, bwul, fsadl, fsbdl, fscdl, fsaul, fsbul, fscul

# Header
print("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % 
    ("DL comb", 
    "DL MIMO", 
    "DL BW", 
    "DL Unk A",  # 4 = mmWave only, 2 = n3, n7, n38, n78, 1 = n1, n7, n8 ,n20, n28
    "DL Unk B",  # 1 = mmWave, 2 = regular
    "DL Unk C",  # 1 = HPUE?, 0 = regular
    "UL comb", 
    "UL MIMO", 
    "UL BW", 
    "UL Unk A", 
    "UL Unk B", # 1 = mmWave, 2 = regular
    "UL Unk C")) # 1 = HPUE?, 0 = regular

# Construct the output
for value in server.a:
    for value1 in value.b:
        dlc = [''.join([('_' if re.match("n.*",i) else '-')+i for i in comboconstructor(value1)[0]])]
        ulc = [''.join([('_' if re.match("n.*",i) else '-')+i for i in comboconstructor(value1)[1]])]
        print("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % 
            # band dl combo
            (dlc[0][1:], 
            # band dl mimo
            ';'.join(map(str, comboconstructor(value1)[2])),
            # band dl bw
            ';'.join(map(str, comboconstructor(value1)[4])),
            # band dl unknown a
            ';'.join(map(str, comboconstructor(value1)[6])),
            # band dl unknown b
            ';'.join(map(str, comboconstructor(value1)[7])),
            # band dl unknown c
            ';'.join(map(str, comboconstructor(value1)[8])),
            # band ul combo
            ulc[0][1:], 
            # band ul mimo
            ';'.join(map(str, comboconstructor(value1)[3])),
            # band ul bw
            ';'.join(map(str, comboconstructor(value1)[5])),
            # band ul unknown a
            ';'.join(map(str, comboconstructor(value1)[9])),
            # band ul unknown b
            ';'.join(map(str, comboconstructor(value1)[10])),
            # band ul unknown a
            ';'.join(map(str, comboconstructor(value1)[11]))))
        #print(comboconstructor(value1)[0], ";", comboconstructor(value1)[2], sum(comboconstructor(value1)[2]), ";", comboconstructor(value1)[1],";", comboconstructor(value1)[3], sum(comboconstructor(value1)[3]))
#comboconstructor(value1)[6], comboconstructor(value1)[7], comboconstructor(value1)[8], comboconstructor(value1)[9], comboconstructor(value1)[10], comboconstructor(value1)[11]