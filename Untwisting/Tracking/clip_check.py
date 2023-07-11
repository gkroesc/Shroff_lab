import numpy as np
import pandas as pd

#be sure to change the volumes
for num in range(9,115):
	csv_num = str(num)
	file = 'Z:\\Cell_Tracking_Project\\Vab-1\\Tracking\\Pos0\\SPIMB\\Reg_Sample\\For_Tracking\\RegB\\Decon_reg_'+csv_num+'\\Decon_reg_'+csv_num+'_results\\integrated_annotation\\annotations.csv'
	df = pd.read_csv(file)
	cells = df['name'].tolist()
	
	str_file = 'Z:\\Cell_Tracking_Project\\Vab-1\\Tracking\\Pos0\\SPIMB\\Reg_Sample\\For_Tracking\\RegB\\Decon_reg_'+csv_num+'\\Decon_reg_'+csv_num+'_results\\straightened_annotation\\straightened_annotations.csv'
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

	

