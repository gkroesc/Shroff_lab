# Copyright 2020 DRVision Technologies LLC.
# SPDX-License-Identifier: CC-BY-NC-4.0
# Edited 11/12/2021 11:30am - matthew.chaw@nih.gov - Edits: Script contained in for loop to iterate through mult. positions. Typos fixed. 

from rcan.utils import apply, get_model_path, normalize, load_model
import argparse
import keras
import numpy as np
import tifffile
import os
import time
from scipy.ndimage import zoom
from scipy.ndimage import rotate

#parser = argparse.ArgumentParser()
#parser.add_argument('-m', '--model_dir', type=str, required=True)
#parser.add_argument('-i', '--input', type=str, required=True)
#parser.add_argument('-o', '--output', type=str, required=True)
#parser.add_argument('-g', '--ground_truth', type=str)
#parser.add_argument('-b', '--bpp', type=int, choices=[8, 16, 32], default=32)
#args = parser.parse_args()




def main():
    #______________________________________________________________________________________________________________________________

    positions = [1] #<--- Put the positions here separated by commas ','. Ex. positions = [0,2,1,3] It does not need to be in order. OMIT ALL SPACES. 
    regs = ['A', 'B']
    #______________________________________________________________________________________________________________________________

    for position in positions:

        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"

        step1_model_dir = 'E:\\Nuclei Model\\Model_step1'
        step2_model_dir = 'E:\\Nuclei Model\\Model_step2'
        prediction_dir = 'I:\\RC_Data_Transfer\\123021_BV514_Dpy7\\BV514xDPY7\\Pos{}\\Reg_Sample'.format(position) 
        # .format() will insert the variable into the brackets at the given position.
        # ex. prediction_dir = 'X:\\Cell_Tracking_Project\\RW10742\\Hyp_Screen\\112221_multi\\Pos{}\\SPIMB\\Reg_Sample'.format(position)  
        
        for reg in regs:

            test_folder = 'Reg{}'.format(reg)
            output_folder1 = 'RCAN_2Step_DL_' + test_folder

            try:
                DL_path = prediction_dir + '\\' + output_folder1
                if not os.path.exists(DL_path):
                    os.makedirs(DL_path)
            except OSError:
                print ("Creation of the directory %s failed" % DL_path)
            else:
                print ("Successfully created the directory %s " % DL_path)

            input_labels=os.listdir(prediction_dir + '\\' + test_folder)
            maxlen = len(input_labels)

            model_path1 = get_model_path(step1_model_dir)
            model_path2 = get_model_path(step2_model_dir)
            print('Loading model from', model_path1)
            print('Loading model from', model_path2)
            overlap_shape = [2, 32, 32]
            model1 = load_model(str(model_path1), input_shape=(52, 128, 128))
            model2 = load_model(str(model_path2), input_shape=(308, 128, 128))

            zoom_z = 6
            #model = keras.models.load_model(str(model_path), compile=False)
            for i in range(0,maxlen):  #maxlen): #<<<<<<----------------------- Change for shorter runs
                time_start=time.time()
                Prediction_File = prediction_dir + '\\' + test_folder + '\\'+ input_labels[i]
                print('Loading raw image from', Prediction_File)
                input_data = tifffile.imread(Prediction_File)
                input_data = input_data[::zoom_z,:,:]
                ndim = input_data.shape

                # Step 1
                result = apply(model1, normalize(input_data), overlap_shape=overlap_shape, verbose=True)
                result[result < 0] = 0
                result = zoom(result, (zoom_z, 1, 1))

                #Step 2

                ndim = result.shape
                result = apply(model2, normalize(result), overlap_shape=overlap_shape, verbose=True)
                inmin, inmax = result.min(),result.max()
                result =(result-inmin)/(inmax-inmin)*65535
                tifffile.imsave(prediction_dir + '\\' + output_folder1 + '\\DL_' + input_labels[i], result.astype('uint16'))

              #  tifffile.imsave(prediction_dir + '\\' + output_folder2 + '\\DL_' + input_labels[i], result.astype('uint16'))
                print(time.time()-time_start)
                #final_result = np.clip(65535 * result, 0, 65535)

                print('Saving output image', input_labels[i])

main()


