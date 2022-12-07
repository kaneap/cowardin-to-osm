# cowardin-to-osm
This tool is for converting Cowardin wetland classification codes into tags for OpenStreetMap. This is meant to assist in imports of wetland data from
the US National Wetland Inventory, which uses the codes to classify every bit of wetland in the dataset.

The Classification of Wetlands and Deepwater Habitats of the United States (here called the Cowardin System) is detailed [here](https://www.fws.gov/media/classification-wetlands-and-deepwater-habitats-united-states)
It is extremely detailed, and the majority of the wetland detail has no equivilant tagging in OSM. Nonetheless, many tags can be derived from the codes.

This uses the NWI wetland definitions available [here](https://www.fws.gov/program/national-wetlands-inventory/classification-codes). A compacted version (without the long wordy descriptions of all the features) is included in this repository, but the default NWI_Code_Definitions.csv available from the USFAWS will work just as well.

Currently only palustrine wetland codes are supported, but it is hoped to support them all eventually.
