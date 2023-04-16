# Pixel-Shannon-Combos
An attempt to decode the new set of configuration files introduced by Google in the first beta release of Android 14 for the Pixel 7 series which included the implementation of Rel 16 3GPP in its Shannon 5300 modem. These configuration files are stored in `/vendor/firmware/uecapconfig` in the form of .binarypb (Protobuf) files.

The configuration files define NR SA and NR NSA carrier aggregation combinations per mobile carrier.

## Note
Please note that this is not a final version as there is still additional functionality defined in the uecapconfig files that I don't fully understand.

## How to Run
To use Pixel-Shannon-Combos, simply provide the configuration file as an argument to the uecaps.py script:

`uecaps.py ./uecapconfig/WILDCARD.binarypb > WILDCARD.csv`

The output will generate a comma-separated value (CSV) file where the left column defines downlink and the right column defines uplink. Here's an example of a line:

`1-3-7C_n28,7_n28`

Previously decompiled csv's can be found in the uecapconfig_csv directory of this repo - note that these were generated on 15th april and could be out of that at the moment you're looking at this.
