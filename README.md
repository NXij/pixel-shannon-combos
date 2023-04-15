# pixel-shannon-combos
A new set of configuration files was introduced by Google on the first beta release of Android 14 for the Pixel 7 series along with the implementation of Rel 16 3GPP in its Shannon 5300 modem.

These configuration files reside in `/vendor/firmware/uecapconfig` in the form of .binarypb (Protobuf) files

NR SA and NR NSA carrier aggregation combinations get defined here per mobile carrier

## Note
This is by no means final as I do not understand many of the functionality defined in the uecapconfig files

## Running
Provide the file as an argument to the uecaps.py script:

`uecaps.py ./uecapconfig/WILDCARD.binarypb > WILDCARD.csv`

The output will create a coma delimited csv file where the left column defines downlink and the right one uplink

Here is an example line

`1-3-7C_n28,7_n28`
