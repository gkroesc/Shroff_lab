import pandas as pd 
import timeit
import math


def predCellLinPairs(df, namecol, lincol):
	'''
	input: dataframe with all cells in scRNA dataset
		   string, name of column that contains cell names
		   string, name of column that contains lineage names
	
	output: nested dictionary containing cellnames and corresponding lineages and their frequency in dataset
			--> {cell1: {lineage1: 5, lineage 2: 4, lineage 3: 24}
				 cell2: {lineage 1: 45}
				 cell3: {lineage 1: 13, lineage 2:1, lineage 3: 1}
				 }
	'''

	cellnames = df[namecol].to_list()
	linnames = df[lincol].to_list()

	pardict = dict()
	#Must not have nan because cell name or corresp. lineage must be matched first. 
	for i in range(len(cellnames)):
		if (str(cellnames[i]) == 'nan') == False and (str(linnames[i]) == 'nan') == False:
			#print(1)
			if cellnames[i] in pardict.keys():
				#print(11)
				#cell is already in pardict
				if linnames[i] in pardict[cellnames[i]]:
					#print(111)
					#lineage is already associated
					pardict[cellnames[i]][linnames[i]] += 1
					#add 1 to count
				else:
					#print(110)
					#lineage is not yet associated.
					pardict[cellnames[i]][linnames[i]] = 1 
					#Create count with start value 1
			else:
				#print(10)
				#Cell is not in the parent dict so there are no lineages associated yet. 
				pardict[cellnames[i]] = dict()
				#Create dictionary for cell in parent dict
				pardict[cellnames[i]][linnames[i]] = 1
				#create lineage directory in cell directory
	return pardict



def main():
	start = timeit.default_timer()

	GSE_cells_path = "C:\\Users\\chawmm\\Desktop\\RNAseq Project\\scRNAseq Data\\Raw\\GSE126954_cell_annotation.csv"
	packer_s6_path = "C:\\Users\\chawmm\\Desktop\\RNAseq Project\\Cell Mapping\\scripts\\gene_ex_to_model\\cellkeys\\packer_s6.csv"
	wack_path = "C:\\Users\\chawmm\\Desktop\\RNAseq Project\\Cell Mapping\\scripts\\gene_ex_to_model\\cellkeys\\WormAtlas Cell Key.csv"
	model_path = "C:\\Users\\chawmm\\Desktop\\RNAseq Project\\Cell Mapping\\scripts\\gene_ex_to_model\\cellkeys\\model_to_lin.csv"
	output_path = "C:\\Users\\chawmm\\Desktop\\RNAseq Project\\Cell Mapping\\scripts\\gene_ex_to_model\\cellkeys"
	
	df = pd.read_csv(GSE_cells_path) 
	modeldf = pd.read_csv(model_path)
	wackdf = pd.read_csv(wack_path)
	packer_s6 = pd.read_csv(packer_s6_path)
	wackdf['Lineage Name'] = wackdf['Lineage Name'].str.replace(" ", "")
	wackdf['Lineage Name'] = wackdf['Lineage Name'].str.lower()
	packer_s6['cell'] = packer_s6['cell'].str.lower() 
	modeldf['lineage'] = modeldf['lineage'].str.lower()
	modeldf['lineage'] = modeldf['lineage'].str.replace(" ", "")


	stop = timeit.default_timer()
	print("{} --> {}s elapsed".format("loaded data", stop-start))


	cell_column_name = "plot.cell.type"
	lineage_column_name = 'lineage'
	celldict = predCellLinPairs(df, cell_column_name, lineage_column_name)
	stop = timeit.default_timer()
	print("{} --> {}s elapsed".format("collected lineage frequencies", stop-start))

	inp = input("View associations? Y/N: ").lower()

	if inp == "y":

		for cell in celldict.keys():
			sumfreq = sum(celldict[cell].values())
			for lineage in celldict[cell].keys():
				print("{} assoc. with {} {} times. {}%".format(cell, lineage, celldict[cell][lineage], 100*celldict[cell][lineage] / sumfreq))
			print('\n')
	else:
		pass

	start = timeit.default_timer()
	key_data = {'data cellname': list(), 'data lineage':list(), 'wormatlas lineage': list()}

	for cell in celldict.keys():
		for lineage in celldict[cell].keys():
			tempdf = packer_s6.isin([lineage])
			isin = packer_s6[packer_s6.isin([lineage])['annotation_name'] == True]['cell'].to_list()
			for actLineage in isin:
				key_data['data cellname'].append(cell)
				key_data['data lineage'].append(lineage)
				key_data['wormatlas lineage'].append(actLineage)
	key = pd.DataFrame(data = key_data)
	wackdf = wackdf[['Cell', 'Lineage Name']]
	wackdf = wackdf.rename(columns = {'Cell': 'wormatlas cellname', 'Lineage Name':'wormatlas lineage'})
	key = key.merge(wackdf, on='wormatlas lineage')
	modeldf = modeldf.rename(columns = {'name':'model cellname', 'lineage':'wormatlas lineage'})
	key = key.merge(modeldf, on='wormatlas lineage')
	
	key.to_csv(output_path+'\\masterkey.csv', index = False)
	stop = timeit.default_timer()
	print("{} --> {}s elapsed".format("Generating Cell Key", stop-start))








main()





