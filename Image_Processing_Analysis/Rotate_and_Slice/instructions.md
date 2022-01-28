# Rotate and Slice for Lineaging

Use this file to prepare a lineaging dataset for AceTree. It rotates all of the images are in canonical orientation and each slice is saved ans an individual image. This should be done after deep learning and normalization have been run on the images, this is the last step before viewing the data in AceTree.

## Setup:
  1. Adjust the path in line 1 up to the For_Lineaging folder
  2. If needed adjust the start value in line 10 to the first timepoint you want to be able to view in AceTree (generally 0)
  3. If needed adjust the redstart value in line 12 to the first timepoint that you want to be able to view the red channel in AceTress (default is 200)
  4. Adjust the twitch value in line 13 to the first timepoint after twitching begins
  5. Use Fiji pulgin TransformJ to determine the degrees that the image must be rotated to get the embryo into canonical oreintation
      -Starting with z,  determine the rotation angle in degrees for the image to be in the correct oreintation on the z axis 
      -Repeat for the y-angle using the image that has already been rotated on the z axis
      -Repeat for the x-angle using the image that has already been rotated on the z and y axes
      -Your image should now have the embryo in canonical orientation, double check by starting with the original image and performing the rotation on all thre axes simultaneously
     -Record these angle measurement 
   6. Adjust the values for x1, y1, and z1 on line 18 with the rotation angles just found
   7. Adjust the value for startslice to be the z-slice where signal first appears **AFTER** rotation
   8. Press run

The output is found in the StarryNite folder that is generated. The images are saved in the tif anf tifr folders and the paths just need to be specified in the Decon_emb1_edited.xml file within your SN_Files directory. 
