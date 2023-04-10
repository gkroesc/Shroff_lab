# Deep Learning Networks:
These are the two Deep Learning networks that are applied to diSPIM images. Our current 3D-RCAN model is used on any datasat that contains only nuclei. Any images with fluorescent structures other than nuclei (membranes, pharyngeal surface, etc.) should use the Densenet model.
## 3D RCAN
Derived from the paper [Three-dimensional residual channel attention networks denoise and sharpen fluorescence microscopy image volumes](https://www.biorxiv.org/content/10.1101/2020.08.27.270439v1). Our specific model features two steps, the first step is de-aberration and the second is deconvolution. The weights for the trained model that we use can be found in the Model_step1 and Model_step2 folders within this repository. When using 3D-RCAN for the first time follow the Dependencies Installation instructions found in the README file of the repository below. If using pretrained model skip to Applying the Model section. 

### Download/Training instructions
Download the 3D-RCAN repository from the AiviaCommunity page that can be accessed [here](https://github.com/AiviaCommunity/3D-RCAN.git).
- Follow the Training instructions found in the README file from that repository
- The environment currently used as of 09/02/2022 contains the following packages:
   ```
   Package              Version
   -------------------- ---------
   absl-py              0.13.0
   astor                0.8.1
   attrs                21.2.0
   cachetools           4.2.4
   certifi              2021.5.30
   charset-normalizer   2.0.12
   colorama             0.4.4
   gast                 0.2.2
   google-auth          1.35.0
   google-auth-oauthlib 0.4.6
   google-pasta         0.2.0
   grpcio               1.40.0
   h5py                 2.10.0
   idna                 3.3
   importlib-metadata   4.8.1
   jsonschema           3.2.0
   Keras                2.2.4
   Keras-Applications   1.0.8
   Keras-Preprocessing  1.1.2
   Markdown             3.3.4
   mock                 4.0.3
   numexpr              2.7.3
   numpy                1.21.2
   oauthlib             3.2.0
   opt-einsum           3.3.0
   pip                  21.2.2
   protobuf             3.18.0
   pyasn1               0.4.8
   pyasn1-modules       0.2.8
   pyrsistent           0.18.0
   PyYAML               5.4.1
   requests             2.27.1
   requests-oauthlib    1.3.1
   rsa                  4.8
   scipy                1.7.1
   setuptools           58.0.4
   six                  1.16.0
   tensorboard          1.15.0
   tensorflow           2.0.0
   tensorflow-estimator 1.15.1
   tensorflow-gpu       1.15.0
   termcolor            1.1.0
   tifffile             2021.8.30
   tqdm                 4.62.3
   typing-extensions    3.10.0.2
   urllib3              1.26.9
   Werkzeug             2.0.1
   wheel                0.37.0
   wincertstore         0.2
   wrapt                1.14.0
   zipp                 3.5.0
   ```
### Applying the Model
The base script for running the model is found in the RCAN_Apply_diSPIM_TwoSteps0.py file. The seq version of this file is an implementation of the script that can run the model on multiple positions or channels sequentially. 

**Base Version Script Adjustments**
- Line 25
   ```
   step1_model_dir = '\path\to\Model_step1'
   ```
- Line 26
   ```
   step2_model_dir = 'path\to\Model_step2'
   ```
- Line 27 
  ```
  predition_dir = 'path\to\input\image\channels'
  ```
- Line 28 
  ```
  test_folder = 'channel'
  ``` 
  - RegA or RegB
  
- Line 53 only needs to be changed if you do not want to apply the model to all images in that folder
  ```
  for i in range(0, maxlen)
  ```
  - Adjust maxlen to the number of the final image you wish to apply to

**Seq Version Script Adjustments**
- Line 29
  ```
  positions = []
  ```
  - Add the **number only** for all of the positions you want to apply the model to, separated by a comma
  
- Line 30
  ```
  regs = []
  ```
  - Add the **letter only** for all of the channels (generally A and B) you want to apply the model to, separated by a comma
    
- The rest of the adjustments that need to be made are the same as for the base version, the only difference is the line numbers 

**Running the script**
- Open up the command line and navigate to the directory where the above file is found. Ensure that you are in the correct virtual environment if necessary and run:

  ```
  python RCAN_Apply_diSPIM_TwoSteps0.py
  ```

- Once runnning you should get this output for each image should look like:

  ```
  Loading raw image from path\to\input\images\file.tiff
  100%|##################################################################################| 24/24 [00:16<00:00,  1.47it/s]
  100%|##################################################################################| 24/24 [01:24<00:00,  3.52s/it]
  113.12280631065369
  ```

## Densenet 
Derived from the paper [Rapid image deconvolution and multiview fusion for optical microscopy](https://www.nature.com/articles/s41587-020-0560-x)This network is used on the green untwisting channel. The pretrained model shared in this directory is for deconvolution of image volumes, and it can be found in the SeamCellModel folder. If training, follow the instructions found in the DeepLearning folder within the repository linked below, if using pretrained model skip to Applying the Model section.



### Setup
The Densenet_SeamCell_DL.py script has been adapted from repository found [here](https://github.com/eguomin/regDeconProject). There is not a requirements file in this repository as our script was adapted from Matlab, the enviroment used to run this model contains the following packages:
```
Package                 Version
----------------------- ----------
absl-py                 0.13.0
astunparse              1.6.3
cached-property         1.5.2
cachetools              4.2.2
certifi                 2021.5.30
charset-normalizer      2.0.6
clang                   5.0
colorama                0.4.6              
cudatoolkit             11.7.0              
cudnn                   8.4.1.50
flatbuffers             1.12
gast                    0.4.0
google-auth             1.35.0
google-auth-oauthlib    0.4.6
google-pasta            0.2.0
grpcio                  1.40.0
h5py                    3.1.0
idna                    3.2
importlib-metadata      4.8.1
keras                   2.6.0
Keras-Preprocessing     1.1.2
Markdown                3.3.4
numpy                   1.19.5
oauthlib                3.1.1
opt-einsum              3.3.0
pip                     21.2.2
protobuf                3.18.0
pyasn1                  0.4.8
pyasn1-modules          0.2.8
python                  3.7.0
requests                2.26.0
requests-oauthlib       1.3.0
rsa                     4.7.2
setuptools              58.0.4
six                     1.15.0
tensorboard             2.6.0
tensorboard-data-server 0.6.1
tensorboard-plugin-wit  1.8.0
tensorflow-estimator    2.6.0
tensorflow-gpu          2.6.0
termcolor               1.1.0
tifffile                2021.8.30
tiffile                 2018.10.18
torch                   1.12.1                   
tqdm                    4.65.0
typing-extensions       3.7.4.3
urllib3                 1.26.6
Werkzeug                2.0.1
wheel                   0.37.0
wincertstore            0.2
wrapt                   1.12.1
zipp                    3.5.0
```

### Applying the Model
The script for running the model is found in the Densenet_SeamCell_DL.py file.

**Script Adjustments**
-Line 25
```
data_dir = 'path\to\input\image\channels'
```
-Line 27
```
test_folder = 'channel'
```
-Line 501
```
train_dir = 'path\to\SeamCellModel'

**Running the script**
- Open up the command line and navigate to the directory where the above file is found. Ensure that you are in the correct virtual environment if necessary and run:
  ```
  python Densenet_SeamCell_DL.py
  ```

- Once runnning you should get this output should be a series of continuosly updating numbers that represents the number of seconds spent on each volume.
  
- Once finished it should display:
  ```
   Done Testing
   ```


## Richardson-Lucy Network
Derived from the paper [Incorporating the image formation process into deep learning improves network performance](https://www.nature.com/articles/s41592-022-01652-7)This network is used on the red untwisting channel. The pretrained model shared in this directory is for deconvolution of image volumes containing both a seam cell nuclear marker and a hypodermal adherens junction marker, it can be found in the RedUntwistingModel folder. If training, follow the instructions found in the repository linked below, if using pretrained model skip to Applying the Model section.



### Setup
The RLN_single.py script has been adapted from repository found [here](https://github.com/MeatyPlus/Richardson-Lucy-Net). The same virtual environment used above for the densenet was used for this network as well.

### Applying the Model
The script for running the model is found in the RLN_single.py file.

**Script Adjustments**
-Line 44
```
train_model_path = 'path\to\RedUntwistingModel'
```
-Line 47
```
data_dir = 'path\to\input\image\channels'
```
-Line 48
```
input_folder = 'channel\'

**Running the script**
- Open up the command line and navigate to the directory where the above file is found. Ensure that you are in the correct virtual environment if necessary and run:
  ```
  python RLN_single.py
  ```

- Once runnning you should get this output that looks like:
  ```
  num 0, runtime:4.755948
  num 1, runtime:4.322918
  ```
- Once finished it should display:
  ```
   Done Testing
  ```

