# Registration

This is the last processing step before images are put through deep learning. It crops down each image and rescales in z so that it has the correct number of slices. Use the split dual-view application if the dual color image splitter was used on the diSPIM and two different colors of fluoresence were used. Use the bypass file if bypass mode was used on the diSPIM and only one color was used for fluoresence


## Split Dual-view Application
### How to open the program:
  1. Copy the folder “splitDualViewReg” to ImageJ or Fiji’s main folder.
  2. Install the UI macro: ImageJ (or Fiji) Plugins--> Macros-->Install..., Choose the macro file “splitDualViewReg_UI.ijm” (within the “splitDualViewReg” folder). Then there will be a splitDualViewReg option listed on the Plugins--> Macros menu.
                             or 
      Directly open the “splitDualViewReg_UI.ijm” within imageJ (or Fiji) and run it;
  3. Make sure that you also have downloaded the CudaApp folder and the path in line 16 correctly points  to the directory that contains the Cuda App

### How to use the program
  1. Run the program: ImageJ (or Fiji) Plugins--> Macros--> splitDualViewReg.
  2. Following the pop-up dialogs, sequentially select folders: 
  For single color: Input folder→Beads Image →Output folder; 
  3. Select Region of Interest: 
  The program pop-up 2 image windows (maximum projections of images), draw rectangles to contain the samples. The images will be cropped automatically based on the rectangles. The cropping will also be implied to the bead images. During the cropping a subtraction of 100 will also be applied to the images. Users can adjust the contrast of each image if needed, but the size of the rectangles should be same. 
  4. Confirm and modify the parameters in the next pop-up panel:
  ![image](https://user-images.githubusercontent.com/84924498/151614690-21908ff0-d97d-4502-907e-53187f4143ad.png)

  6. If “Customized” is selected for initial matrix, then users would be guided to choose a matrix file.
  7. Then the macro calls GPU-based applications. And once the running is completed, all messages will show up in the imageJ log window.
  8. The final outputs are within the folder “Reg_Sample”


Please note: if it’s the first time for the GPU device to run on the computer, it may take some time (up to minutes) to initialize the device. But once the device is initialized, it won’t need initialization next time.


## Bypass Registration

### How to open the program:
  1. Download the BypassReg.ijm file and directly open it within Fiji
  
### Before running the program:
  1. Adjust the Path in line 5 of the file, stop after SPIMB or SPIMA. Be sure to use double backslashes (\\) in between directories
  2. Adjust the first and second number in line 9 to be the first and last timepoint that you wish to register
  3. Open the max projection for that specific position and draw a 325x425 square that contains the embryo in it. Record the x and y dimensions of that box and update line 11 with these dimentsions

Press run, output will be saved in a RegA folder with the prefix C1_reg
