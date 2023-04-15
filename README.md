# pixel-shannon-combos
A new set of configuration files was introduced by Google on the first beta release of Android 14 for the Pixel 7 series.

These configuration files reside in `/vendor/firmware/uecapconfig` in the form of .binarypb (Protobuf) files

NR SA and NR SA carrier aggregation combinations get defined here per mobile carrier

## Running
Provide the file as an argument to the uecaps.py script:

`uecaps.py ./uecapconfig/WILDCARD.binarypb > WILDCARD.csv`

The output will create a coma delimited csv file where the left column defines downlink and the right one uplink

Here is an example line

`1-3-7C_n28,7_n28`
