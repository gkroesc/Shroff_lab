import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


full_model_vis_path = "C:\\Users\\kroeschellga\\Desktop\\C-Elegans-Model-Generation-full\\C-Elegans-Model-Generation-7be08090c5136fdb61a6bdbe80266bf70a2d9e26\\workspace\\2022_06_16-Full_Model_Updated"

stripped_model_vis_path = "C:\\Users\\kroeschellga\\Desktop\\C-Elegans-Model-Generation-full\\C-Elegans-Model-Generation-7be08090c5136fdb61a6bdbe80266bf70a2d9e26\\workspace\\2022_06_22-Full_Model_RW10711_Stripped_v2"

cells = ['adal','adar','adel','ader','aizl','aizr','avdl','canl','flpl','flpr','rmgl','rmgr']

for cell in cells:

	full_coord_df = pd.read_csv(full_model_vis_path + "\\output\\" + cell + ".csv", header = None,  usecols=[0,1,2,3])

	full_coord_df.columns = ["Time","X voxels","Y voxels","Z voxels"]

	stripped_coord_df = pd.read_csv(stripped_model_vis_path + "\\output\\" + cell + ".csv", header = None,  usecols=[0,1,2,3])

	stripped_coord_df.columns = ["Time","X voxels","Y voxels","Z voxels"]


	x = full_coord_df["Time"]

	fig, ((ax1, ax2), (ax3, ax4), (ax5,ax6)) = plt.subplots(3,2, sharex=True, sharey='row')

	fig.set_size_inches(12,10)

	fig.suptitle(cell)

	ax1.plot(x, full_coord_df["X voxels"])
	ax1.set_title('Full Model')
	ax1.set_ylabel('X voxels')
	ax2.plot(x, stripped_coord_df["X voxels"])
	ax2.set_title('Missing SC')
	ax3.plot(x,full_coord_df["Y voxels"])
	ax3.set_ylabel('Y voxels')
	ax4.plot(x, stripped_coord_df["Y voxels"])
	ax5.plot(x, full_coord_df["Z voxels"])
	ax5.set_ylabel('Z voxels')
	ax6.plot(x, stripped_coord_df["Z voxels"])


	fig.tight_layout()


	plt.show()

