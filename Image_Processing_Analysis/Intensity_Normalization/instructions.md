# Intensity Normalization

These codes can be run on image files AFTER they have gone through deep learning. It zeros the background intensity and reduces signal to levels that allows for the best visualization in AceTree/MIPAV. It also renames the image files and switches the RegA/RegB folders.......

All are used by dragging and dropping the file into Fiji which opens the interacive macro editor

## Lineage Normalization

This is run on a lineaging dataset where both channels have gone through the 3D-RCAN two step deep learning network. One should be a pan-nuclear channel and the other should be  a different color expressed in the cells that you are interested in lineaging.

### Setup:
  1. Adjust the path in line 5 to point to where your image files are located, Up until the directory where the deep learning results folders are located
  2. Adjust the first and second numbers in line 11 to be the first and last timepoints of interest
  3. Press run

The output is found in a For_Lineaging folder. This output must be put through the rotate and slice macro before it can be viewed in AceTree

## Tracking Normalization

This is run on a tracking dataset where both channels have gone through deep learning. One should be the untwisting channel (Seam cell and pharyngeal surface marker fluoresecence) that went through the Densenet Deconvolution network. The other should be the tracking channel (expression in the nuclei of selected cells) that has already gone through the 3D-RCAN two step deep learning network.

### Setup:
  1. Adjust the path in line 5 to point to where your image files are located, Up until the directory where the deep learning results folders are located
  2. Adjust the first and second numbers in line 11 to be the first and last timepoints of interest
  3. Press run

The output is located in the For_Tracking folder. These images are ready to be loaded into MIPAV for 3D viewing.

## Single View Normalization

This is run on any dataset where bypass mode was used and there is only one channel to normalize. 

### Setup:
  1. Adjust the path in line 2 up to the position you wish to normalize and rename
  2. Adjust the first and second numbers in line 7 to be the first and last timepoints of interest
  3. Press Run

The output is located in the For_Tracking/RegB folder. These images are ready to be loaded into MIPAV for 3D viewing



