# Intensity Normalization

These codes can be run on image files AFTER they have gone through deep learning. It zeros the background intensity and reduces signal to levels that allows for the best visualization in AceTree/MIPAV. It also renames the image files and switches the RegA/RegB folders.......

All are used by dragging and dropping the file into Fiji which opens the interacive macro editor. Once open press run and a dialog box should pop up where you can specify details of the imaging run

## Lineaging Normalization

This is run on a lineaging dataset where both channels have gone through the 3D-RCAN two step deep learning network. One should be a pan-nuclear channel and the other should be  a different color expressed in the cells that you are interested in lineaging/tracking.

The output is found in a For_Lineaging folder. This output must be put through the rotate and slice macro before it can be viewed in AceTree

## Tracking Normalization

This is run on a tracking dataset where both channels have gone through deep learning. One should be the untwisting channel (Seam cell and pharyngeal surface marker fluoresecence) that went through the Densenet Deconvolution network. The other should be the tracking channel (expression in the nuclei of selected cells) that has already gone through the 3D-RCAN two step deep learning network.

The output is located in the For_Tracking folder. These images are ready to be loaded into MIPAV for 3D viewing.

## Single View Normalization

This is run on any dataset where bypass mode was used and there is only one channel to normalize. 


The output is located in the For_Tracking/RegB folder. These images are ready to be loaded into MIPAV for 3D viewing


