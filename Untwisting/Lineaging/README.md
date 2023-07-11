# Lineaging

These are the different codes associated with Cell Lineaging using the application AceTree. All the code necessary to run the app as well as set up instructions can be found [here](https://github.com/zhirongbaolab/AceTree.git).  

The ImageJ macro that converts image files into the correct format to load into Acetree can be found [here](https://github.com/gkroesc/Worm_untwisting_project/tree/main/Image_processing/Rotate_and_Slice), in the Image Processing folder of this repository. 

## Cell Namer

The cellNamer.py script takes a MIPAV annotations.csv file and converts the lineage name to the function name. This allows for easy identification of cells when the Acetree data is loaded into MIPAV. 

The script requires the cellKeyMaster.csv file and an input annotations.csv file in the same directory as the script itself. The output should be called updated_annotations.csv in that same folder. In order to view these updates in MIPAV this output needs to be moved to the integrated_annotations folder in the RegB folder of the image files.

## AT_to_MIPAV

This is a short ImageJ macro that converts the individual tif input slices from Acetree into full stacks for viewing in MIPAV. Processes entire folder, will only work if starting from the first timepoint. If you wish to start at a later timepoint you will need to generate new tif and tifr input folders that contain all slices on from the timepoint that you wish to start at. 
