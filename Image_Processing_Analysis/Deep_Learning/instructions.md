# Deep Learning Networks:
These are the two Deep Learning networks that are applied to diSPIM images. Our current 3D-RCAN model is used on any datasat that nuclei only. Any images with fluorescent structures other than nuclei (membranes, pharyngeal surface, etc.) should use the Densenet model.
## 3D RCAN
Derived from the paper [Three-dimensional residual channel attention networks denoise and sharpen fluorescence microscopy image volumes](https://www.biorxiv.org/content/10.1101/2020.08.27.270439v1). It was trained on datasets found in the (blank) folder that consist of fluorescent nuclei. 

### Download/Training instructions
Download the 3D-RCAN repository from the AiviaCommunity page that can be accessed [here](https://github.com/AiviaCommunity/3D-RCAN.git).
Refer to the requirements.txt file in the repository for creating an environment with the correct packages/versions
- If using your own data to train a new model follow the instructions in the README file from that repository
- If using existing model proceed to the next section

### Applying the Model


## Densenet 
