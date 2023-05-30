# Pixel-Shannon-Combos
An attempt to decode the new set of configuration files introduced by Google in the first beta release of Android 14 for the Pixel 7 series which included the implementation of Rel 16 3GPP in its Shannon 5300 modem. These configuration files are stored in `/vendor/firmware/uecapconfig` in the form of .binarypb (Protobuf) files.

The configuration files define NR SA and NR NSA carrier aggregation combinations per mobile carrier.

## Note
Please note that this is not a final version as there is still additional functionality defined in the uecapconfig files that I don't fully understand.

## How to Run
To use Pixel-Shannon-Combos, simply provide the directory with the .binarypb files as the first parameter and the second one as the output directory.

`./uecaps.py ./uecapconfig_a14_b22 ./uecapconfig_csv`

The output will generate a comma-separated value (CSV with headers) file with most of the values found in the binarypb files:

`DL comb	DL MIMO	DL BW	DL Unk A	DL Unk B	DL Unk C	UL comb	UL MIMO	UL BW	UL Unk A	UL Unk B	UL Unk C`

`2-13_n2_n77C	2;2;2	40;80;80	1;2;2	2;2;2	0;0;0	2_n77	1	50	2	2	0`

Note that the output files can get rather big

Previously decompiled csv's can be found in the uecapconfig_csv directory of this repo - note that these were generated on April 15th and could be out of date at the moment you're looking at this. uuecapconfig_csv_full firectory has the decoded output from the 14 Beta 2.1.
