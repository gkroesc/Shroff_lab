# Copyright 2020 DRVision Technologies LLC.
# SPDX-License-Identifier: CC-BY-NC-4.0

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

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

step1_model_dir = 'C:\\Users\\kroeschellga\\Shroff_lab\\Image_Processing_Analysis\\Deep_Learning\\Model_step1'
step2_model_dir = 'C:\\Users\\kroeschellga\\Shroff_lab\\Image_Processing_Analysis\\Deep_Learning\\Model_step2'
predition_dir = 'C:\\Users\\kroeschellga\\Shroff_lab\\Image_Processing_Analysis\\Deep_Learning\\example_data_rcan'
test_folder = 'RegA'
output_folder1 = 'RCAN_2Step_DL_' + test_folder

try:
    DL_path = predition_dir + '\\' + output_folder1
    if not os.path.exists(DL_path):
        os.makedirs(DL_path)
except OSError:
    print ("Creation of the directory %s failed" % DL_path)
else:
    print ("Successfully created the directory %s " % DL_path)

input_labels=os.listdir(predition_dir + '\\' + test_folder)
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
for i in range(0, maxlen):  #maxlen):
    time_start=time.time()
    Predition_File = predition_dir + '\\' + test_folder + '\\'+ input_labels[i]
    print('Loading raw image from', Predition_File)
    input_data = tifffile.imread(Predition_File)
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
    tifffile.imsave(predition_dir + '\\' + output_folder1 + '\\DL_' + input_labels[i], result.astype('uint16'))

  #  tifffile.imsave(predition_dir + '\\' + output_folder2 + '\\DL_' + input_labels[i], result.astype('uint16'))
    print(time.time()-time_start)
    #final_result = np.clip(65535 * result, 0, 65535)

    print('Saving output image', input_labels[i])


