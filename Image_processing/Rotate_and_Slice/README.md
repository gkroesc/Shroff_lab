# Rotate and Slice for Lineaging

Use this file to prepare a lineaging dataset for AceTree. It rotates all of the images are in canonical orientation and each slice is saved ans an individual image. This should be done after deep learning and normalization have been run on the images, this is the last step before viewing the data in AceTree.

## Setup:

**Image Rotation**

This program requires you to enter the degrees that the image must be rotated to get the embryo into canonical oreintation

This is easiest to determine using the [TransformJ](https://imagescience.org/meijering/software/transformj/) plugin for imageJ and following these steps:
1. Starting with z,  determine the rotation angle in degrees for the image to be in the correct oreintation on the z axis 
2. Repeat for the y-angle using the image that has already been rotated on the z axis
3. Repeat for the x-angle using the image that has already been rotated on the z and y axes
4. Your image should now have the embryo in canonical orientation, double check by starting with the original image and performing the rotation on all thre axises simultaneously
5. Record these angle measurments and the z-slice where signal first appears **AFTER** rotation
 
Once these values are determined, drag and drop this file into Fiji which opens the interactive macro editor. Once open press run and a dialog box should pop up where you can specify input filepaths and details of the imaging run including these four values from above.


The output is found in the StarryNite folder that is generated. The images are saved in the tif anf tifr folders and the paths just need to be specified in the Decon_emb1_edited.xml file within your SN_Files directory. 
