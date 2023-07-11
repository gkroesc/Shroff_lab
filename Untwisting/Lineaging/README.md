# Lineaging

These are the different codes associated with Cell Lineaging using the application AceTree. All the code necessary to run the app as well as set up instructions can be found [here](https://github.com/zhirongbaolab/AceTree.git).  

The ImageJ macro that converts image files into the correct format to load into Acetree can be found [here](https://github.com/gkroesc/Worm_untwisting_project/tree/main/Image_processing/Rotate_and_Slice), in the Image Processing folder of this repository. 

## AceTree to MIPAV

Set of two codes that convert AceTree data into a MIPAV friendly format so that the lineage can easily be viewed in 3D. AT_to_MIPAV.ijm is an ImageJ macro that converts individua  

## Cell Namer

The cellNamer.py script takes a MIPAV annotations.csv file and converts the lineage name to the function name. This allows for easy identification of cells when the Acetree data is loaded into MIPAV. 

The script requires the cellKeyMaster.csv file and an input annotations.csv file in the same directory as the script itself. The output should be called updated_annotations.csv in that same folder. In order to view these updates in MIPAV this output needs to be moved to the integrated_annotations folder in the RegB folder of the image files.


