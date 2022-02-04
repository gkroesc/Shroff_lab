# Deep Learning Networks:
These are the two Deep Learning networks that are applied to diSPIM images. Our current 3D-RCAN model is used on any datasat that contains only nuclei. Any images with fluorescent structures other than nuclei (membranes, pharyngeal surface, etc.) should use the Densenet model.
## 3D RCAN
Derived from the paper [Three-dimensional residual channel attention networks denoise and sharpen fluorescence microscopy image volumes](https://www.biorxiv.org/content/10.1101/2020.08.27.270439v1). The weights for the trained model that we use can be found in the Model_step1 and Model_step2 folders within this repository. When using 3D-RCAN for the first time follow the Dependencies Installation instructions found in the README file of the repository below. If using pretrained model skip to Applying the Model section. 

### Download/Training instructions
Download the 3D-RCAN repository from the AiviaCommunity page that can be accessed [here](https://github.com/AiviaCommunity/3D-RCAN.git).
- Follow the Training instructions found in the README file from that repository

### Applying the Model
The base script for running the model is found in the RCAN_Apply_diSPIM_TwoSteps0.py file. The many version of this file is an implementation of the script that can run the model on multiple positions or channels sequentially. 

**Base Version Script Adjustments**
- Line 25
   '''
   step1_model_dir = '\path\to\Model_step1'
   '''
- Line 26
   '''
   step2_model_dir = 'path\to\Model_step2'
   '''
- Line 27 
  '''
  predition_dir = 'path\to\input\image\channels'
  '''
- Line 28
  - '''test_folder = 'channel'''' (RegA or RegB)
- Line 53 only needs to be changed if you do not want to apply the model to all images in that folder
  - '''for i in range(0, maxlen)'''
  -  Adjust maxlen to the number of the final image you wish to apply to

Once the script is ready, open up the command line and navigate to the directory where the above file is found. Ensure that you are in the correct virtual environment if necessary and run:

'''python RCAN_Apply_diSPIM_TwoSteps0.py'''

Once runnning you should get this output for each image should look like:

'''Loading raw image from path\to\input\images\file.tiff
100%|##################################################################################| 24/24 [00:16<00:00,  1.47it/s]
100%|##################################################################################| 24/24 [01:24<00:00,  3.52s/it]
113.12280631065369'''

## Densenet 
