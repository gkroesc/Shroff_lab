# Rotate and Slice.ijm

Use this file to prepare a lineaging dataset for AceTree. It rotates all of the images are in canonical orientation and each slice is saved ans an individual image. This should be done after deep learning and normalization have been run on the images, this is the last step before viewing the data in AceTree.

## Setup:

**Image Rotation**

This program requires you to enter the degrees that the image must be rotated to get the embryo into canonical orientation

This is easiest to determine using the [TransformJ](https://imagescience.org/meijering/software/transformj/) plugin for imageJ and following these steps:
1. Starting with z,  determine the rotation angle in degrees for the image to be in the correct oreintation on the z axis 
2. Repeat for the y-angle using the image that has already been rotated on the z axis
3. Repeat for the x-angle using the image that has already been rotated on the z and y axes
4. Your image should now have the embryo in canonical orientation, double check by starting with the original image and performing the rotation on all thre axises simultaneously
5. Record these angle measurments and the z-slice where signal first appears **AFTER** rotation
 
Once these values are determined, drag and drop this file into Fiji which opens the interactive macro editor. Once open press run and a dialog box should pop up where you can specify input filepaths and details of the imaging run including these four values from above.


The output is found in the StarryNite folder that is generated. The images are saved in the tif anf tifr folders and the paths just need to be specified in the Decon_emb1_edited.xml file within your SN_Files directory. 

# Slice_Saver.ijm

Short macro for when slice saving needs to be done on a single channel after images have already been rotated, it also normalizes and saves the slices as 8-bit. This is most useful when StarryNite was run on a single channel, and the images from the other channel need to be set up so that both can be viewed and edited in AceTree. 

## Setup:

Drag and drop this file into fiji and press run in the macro editor window, a dialoge box will appear where you specify the path to the rotated images and other parameters like the first and last timepoint and slice. 

The output is placed into a tifr folder generated within the input filepath. This folder can be placed next to the tif folder that is output from StarryNite in order to view both colors simultanweously in AceTree.
