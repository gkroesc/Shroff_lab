# Lineaging

These are the different codes associated with Cell Lineaging using the application AceTree. All the code necessary to run the app as well as set up instructions can be found [here](https://github.com/zhirongbaolab/AceTree.git).  

The ImageJ macro that converts image files into the correct format to load into Acetree can be found [here](https://github.com/gkroesc/Worm_untwisting_project/tree/main/Image_processing/Rotate_and_Slice), in the Image Processing folder of this repository. 

## AceTree to MIPAV

Set of two codes that convert AceTree data into a MIPAV friendly format so that the lineage can easily be viewed in 3D. Both scripts assume the following basic folder structure of AceTree data:
```
StarryNite/: 
  |--SN_Files/: 
     |--Decon_emb1_edited.xml/: 
     |--Decon_emb1_edited.zip/: 
  |--tif/: 
  |--tifr/: 
```
### AT_to_MIPAV.ijm

An ImageJ macro that converts the tif and tifr folders from AceTree into individual image stacks for each timepoint. The user should just be able to press run and they will be prompted with a dialogue box to specify the parent directory containing the tif and tifr image folders. After this there is a second dialogue box in which the user can set the starting timepoint and the first timepoint with red signal as well as the ending timepoint and the number of z slices per timepoint. Processing should automatically start after OK is selected in the second dialogue box. 

**This macro will only work if processing from the first timepoint. If you would like to set start timepoint as a later one, you will need to create a new tif folder that only contains the image slices from your desired starting timepoint and on.**

### Annotations_AT_to_mipav.py

A python script designed to extract cell identities and coordinates from the AceTree nuclei files and convert them into an annotations.csv file that MIPAV can read. There is also a built in naming function that will change a lineage name to a common name if the cell is terminally differentiated (i.e. ABplapaaaapp becomes ADAL).

If using for the fist time the path to cellKeyMaster in line 63 needs to be adjusted to point to the cellkeyMaster.csv file found in the CellNamer subfolder of this directory. Other than that the only changes that need to be made are to start and end timepoint on lines 11 and 13 to match the timepoints you are interested in, and to the zip_path in line 8 to point to your StarryNite parent directory. Also it is good to check that your zip file name matches that of the code: **Decon_emb_edited.zip** or you change the filepath in line 27 of the code to match your zip file name. 

To run this script open an Anaconda prompt, navigate to the directory that it is in and type: `python Annotations_AT_to_mipav.py`

The output of both of these codes is found in a For_mipav folder generated within the StarryNite folder, the default naming for annotation and image files is Decon_reg_#. The RegA and RegB folders within this directory should be ready for loading into MIPAV.

### CellNamer
This folder allows you to run the built in naming function from the above script on a single annotations csv file outside the full code if necessary. Placing an annotation.csv file into this CellNamer folder and then running cellNamer.py outputs an updated_annotations.csv file in the same folder with terminally differentiated cell names updated. 




