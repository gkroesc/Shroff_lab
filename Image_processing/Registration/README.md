# Registration

This is the last processing step before images are put through deep learning. It performs registration of dual-view images so that the two colors align when overlayed. Additionally it crops down each image and rescales z so that pixels are scaled isotropically. All are used by dragging and dropping the file into Fiji which opens the interacive macro editor. Once open press run and a dialog box should pop up where you can specify input filepaths and details of the imaging run.

## Split Dual-view Application
Use this version if the dual color image splitter was used on the diSPIM and two different colors of fluoresence were imaged simultaneously. If using for the first time you must adjust the CUDA app path to match the location where you downloaded this repository on line 16 of the macro.
```
appPath = "\\path\to\repository\Worm_untwisting_project\Image_processing\Registration\CudaApp\"
```

You will be prompted with two max projections, one from each channel, and a pop up instructing you to press OK when the correct region of interest is selected. Use the rectangle tool to draw a 325x425 box around the embryo, making sure to keep all signal within the edges of the box. Once this is done for one of the channels press Ctrl + Shift + E on the keyboard to copy that same sized box onto the other max projection. Once the second box is adjusted to fit the entire embryo, press OK to start running.

The final outputs are in a RegA and RegB folder within a Reg_sample folder, image files will either have the prefix C1 or C2.

More detailed instructions can be found in the SimpleManual.pdf file.

**New Update as of 03/30/2023**

There is now a variable zFlip specified on line 23 of the macro. Set = 0 if there is no z flipping necessary for the imaging system (NIH dispim), set = 1 if images are flipped in z (Janelia dispim). For a new system this will have to be determined empirically.

## Bypass Cropping and Reslicing
There are two options for when only one color was image and registration is not necessary. Use single_reg when dual view was used on the diSPIM but you only want to process one of the channels. Use BypassCropRescale when the diSPIM was used in Bypass mode.

You will be prompted with a single max projection and a pop up instructing you to press OK when the correct region of interest is selected. Use the rectangle tool to draw a 325x425 box around the embryo, making sure to keep all signal within the edges of the box. Once positioned correctly press OK to start running.
  
The output will be saved in a RegA folder, image files have the prefix C1




The output of either of these should be images that are ready to be run through deep learning. 
