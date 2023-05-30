#!/usr/bin/env python
import uecaps_pb2 as uecaps_pb2
import re
import string
import csv
import os
import argparse
import io
import time

parser = argparse.ArgumentParser(description='Dump uecaps')
parser.add_argument('input_dir', type=str, help="Provide the uecaps files directory")
parser.add_argument('output_dir', type=str, help="Provide the output directory")
args = parser.parse_args()

# While decompiling the protobuf, the NR band gets a leading group of numbers in the form of "100"
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
    dlist = [dlcombohandler(value2.band, value2.dlcc) for value2 in combo.c]
    ulist = [ulcombohandler(value2.band, value2.ulcc) for value2 in combo.c if ulcombohandler(value2.band, value2.ulcc) is not None]

    fsdl, fsul, bwdl, bwul, fsadl, fsbdl, fscdl, fsaul, fsbul, fscul = ([] for i in range(10))

    for value2 in combo.c:
        fs_dl = featuresetcontructor(value2.fsdl, 0)
        if fs_dl:
            fsdl += fs_dl[0]
            bwdl += fs_dl[1]
            fsadl += fs_dl[2]
            fsbdl += fs_dl[3]
            fscdl += fs_dl[4]
        fs_ul = featuresetcontructor(value2.fsul, 1)
        if fs_ul:
            fsul += fs_ul[0]
            bwul += fs_ul[1]
            fsaul += fs_ul[2]
            fsbul += fs_ul[3]
            fscul += fs_ul[4]

    return dlist, ulist, fsdl, fsul, bwdl, bwul, fsadl, fsbdl, fscdl, fsaul, fsbul, fscul

# Header
header = [
    "DL comb", 
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
    "UL Unk C"] # 1 = HPUE?, 0 = regular

# Construct the output
def format_output(value1):
    dlist, ulist, fsdl, fsul, bwdl, bwul, fsadl, fsbdl, fscdl, fsaul, fsbul, fscul = comboconstructor(value1)
    dlc = ''.join([('_' if re.search("n.*", i) else '-') + i for i in dlist])
    ulc = ''.join([('_' if re.match("n.*", i) else '-') + i for i in ulist])
    return (dlc[1:], 
            ';'.join(map(str, fsdl)),
            ';'.join(map(str, bwdl)),
            ';'.join(map(str, fsadl)),
            ';'.join(map(str, fsbdl)),
            ';'.join(map(str, fscdl)),
            ulc[1:], 
            ';'.join(map(str, fsul)),
            ';'.join(map(str, bwul)),
            ';'.join(map(str, fsaul)),
            ';'.join(map(str, fsbul)),
            ';'.join(map(str, fscul)))


unixtime = int(time.time())
os.makedirs(os.path.join(args.output_dir, f"dec_{unixtime}"), exist_ok=True)

i = 0
for entry in os.scandir(args.input_dir):
    if entry.is_file() and entry.name.endswith('.binarypb'):
        input_path = entry.path
        with open(input_path, mode='rb') as file:
            fileContent = file.read()
            server = uecaps_pb2.a()
            server.ParseFromString(fileContent)
            output_path = os.path.join(args.output_dir, f"dec_{unixtime}", entry.name) + ".csv"
            i += 1
            print('\rFile: {}'.format(i), end='')
            with io.StringIO(newline='') as output_buffer:
                writer = csv.writer(output_buffer)
                writer.writerow(header)
                for value in server.a:
                    for value1 in value.b:
                        writer.writerow(format_output(value1))
                with open(output_path, 'w', newline='') as output_file:
                    output_file.write(output_buffer.getvalue())