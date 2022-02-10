# Registration

This is the last processing step before images are put through deep learning. It crops down each image and rescales in z so that it has the correct number of slices.  


## Split Dual-view Application
Use this version if the dual color image splitter was used on the diSPIM and two different colors of fluoresence were imaged.

### How to open the program:
  1. Copy the folder “splitDualViewReg” to Fiji’s main folder.
  2. Install the UI macro: Fiji Plugins--> Macros-->Install..., Choose the macro file “splitDualViewReg_UI.ijm” (within the “splitDualViewReg” folder). Then there will be a splitDualViewReg option listed on the Plugins--> Macros menu.
                             or 
      Directly open the “splitDualViewReg_UI.ijm” within Fiji and run it;
  3. Make sure that you also have downloaded the CudaApp folder and the path in line 16 correctly points to the directory that contains the CudaApp
    

### How to use
  1. Run the program: Fiji Plugins--> Macros--> splitDualViewReg.
  2. Following the pop-up dialogs, sequentially select folders: 
  For single color: Input folder→Beads Image →Output folder; 
  3. Select Region of Interest: 
  The program pop-up 2 image windows (maximum projections of images), draw rectangles to contain the samples. The images will be cropped automatically based on the rectangles.   The cropping will also be implied to the bead images. During the cropping a subtraction of 100 will also be applied to the images. Users can adjust the contrast of each image if needed, but the size of the rectangles should be same. 
  4. Confirm and modify the parameters in the next pop-up panel:
  ![image](https://user-images.githubusercontent.com/84924498/151614690-21908ff0-d97d-4502-907e-53187f4143ad.png)

  6. If “Customized” is selected for initial matrix, then users would be guided to choose a matrix file.
  7. Then the macro calls GPU-based applications. And once the running is completed, all messages will show up in the imageJ log window.
  
The final outputs are within the folder “Reg_Sample”

Please note: if it’s the first time for the GPU device to run on the computer, it may take some time (up to minutes) to initialize the device. But once the device is initialized, it won’t need initialization next time.


## Bypass Registration
Use this version if bypass mode was used on the diSPIM and only one color was used for fluorescence.

### How to use

 Download the BypassReg.ijm file and directly open it within Fiji or drag and drop the file directly into Fiji
  
The output will be saved in a RegA folder with the prefix C1_reg

The output of either of these should be images that are ready to be run through deep learning. Eiter 3D-RCAN for images on nuclei or Decon Densenet for anything other than nuclei data
