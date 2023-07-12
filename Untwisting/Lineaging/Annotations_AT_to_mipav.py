import os
import zipfile
import pandas as pd 
import numpy as np



zip_path = "X:\\shrofflab\\efn-1\\lineaging\\For_Lineaging\\StarryNite\\"


start_tp = 10

end_tp = 15

p1_end_tp = end_tp +1

def Acetree_to_MIPAV(zip_path, timepoint):

    columns=['name','x_voxels','y_voxels','z_voxels','R','G','B']

    if not os.path.exists(zip_path + "For_mipav\\RegB\\Decon_reg_{}\\Decon_reg_{}_results\\integrated_annotation".format(timepoint,timepoint)):
        os.makedirs(zip_path + "For_mipav\\RegB\\Decon_reg_{}\\Decon_reg_{}_results\\integrated_annotation".format(timepoint,timepoint))


    def FileGrabber(zip_path, timepoint):

        with zipfile.ZipFile(zip_path + 'SN_Files\\Decon_emb1_edited.zip', 'r') as zip_file:

            ztimepoint = str(timepoint).zfill(3)

            file_path = 'nuclei/t{}-nuclei'.format(ztimepoint)

            with zip_file.open(file_path, 'r') as text_file:

                lines = [line.decode('utf-8').strip() for line in text_file]

            df = pd.DataFrame([line.split(', ') for line in lines])

        return df




    def row_extractor(input_df):
        new_df = pd.DataFrame(columns=columns)

        for index, row in input_df.iterrows():

            if row[9]:

                column9_value = row[9]
                column5_value = row[5]
                column6_value = row[6]
                column7_value = row[7]

                new_row = {'name':column9_value, 'x_voxels': column5_value, 'y_voxels':column6_value, 'z_voxels':column7_value, 'R':255, 'G':255, 'B':255}
                new_row_df = pd.DataFrame(new_row, index=[0])
                new_df = pd.concat([new_df, new_row_df],ignore_index=True)
        return new_df

    def cellNamer(input_df):
    
        cellKeyMaster = 'C:\\Users\\kroeschellg\\Downloads\\Worm_untwisting_project_old\\Segmentation\\Lineaging\\CellNamer\\cellkeyMaster.csv'
        seam_cells = ['H0L','H1L','H2L','V1L','V2L','V3L','V4L','V5L','V6L','TL','H0R','H1R','H2R','V1R','V2R','V3R','V4R','V5R','V6R','TR']


        masterDF = pd.read_csv(cellKeyMaster)
        masterDF.dropna(inplace = True)
        masterKey = masterDF.to_numpy()

    
    
        userAnnotDF = input_df
        userKey = userAnnotDF.to_numpy()
        updateduserKey = userAnnotDF.to_numpy()
        threeNameList = []
        for i, linName in enumerate(userKey[:, 0]):
            for j, name in enumerate(masterKey[:,1]):
                lowlinName = linName.lower().strip()
                namerep = name.replace(" ", "").lower()
                if lowlinName == namerep:
                    threeName = masterKey[j,0]
                    if threeName in seam_cells:
                        updateduserKey[i,0] = threeName
                    else:
                        updateduserKey[i,0] = threeName.lower()
                    #threeNameList.append(threeName)


        Updated_DF = pd.DataFrame(updateduserKey, columns=columns)




        return Updated_DF


    AT_df = FileGrabber(zip_path, timepoint)


    new_df = row_extractor(AT_df)



    named_df = cellNamer(new_df)



    named_df.to_csv(zip_path + "For_mipav\\RegB\\Decon_reg_{}\\Decon_reg_{}_results\\integrated_annotation\\annotations.csv".format(timepoint,timepoint), index=None)


for i in range(start_tp,p1_end_tp):
    Acetree_to_MIPAV(zip_path,i)
