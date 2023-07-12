import numpy as np
import pandas as pd
import os

path = 'X:\\shrofflab\\CND-1_RedUntwisting_A\\Tracking\\032423\\CND-1_RedUT\\Pos2\\SPIMA\\Reg_Sample\\For_Tracking\\RegB'

start_tp = 4

end_tp = 89

p1_end_tp = end_tp + 1

#be sure to change the volumes
for num in range(start_tp, p1_end_tp):
	csv_num = str(num)
	try:
		#npath= 'Y:\\EM_Visualization\\MIPAV_EM_Volume\\Vol2_RegB\\Decon_reg_1\\Decon_reg_1_results\\integrated_annotation\\annotations.csv'
		working_path = path + '\\Decon_reg_'+csv_num+'\\Decon_reg_'+csv_num+'_results'
		file = working_path + '\\integrated_annotation\\annotations.csv'
		os.path.exists(file)
		df = pd.read_csv(file)
		cells = df['name'].tolist()
	
		str_file = working_path + '\\straightened_annotations\\straightened_annotations.csv'
		str_df = pd.read_csv(str_file)
		str_cells = str_df['name'].tolist()
	
		dup_list = []
		new_list = []

		for cell in cells:
			if cell not in str_cells:
				print(cell + ' is clipped out of volume ' + csv_num)
			else:
				continue

			if cell not in new_list:
				new_list.append(cell)
			else:
				dup_list.append(cell)

			if len(dup_list) == 0:
				continue
			else:
				print(dup_list + ' are duplicates at timepoint ' + csv_num)
	except FileNotFoundError:
		print(file + ' does not exist')
		pass

	
	

