'''
applying 4DT to plotly]


just get all coords into long form...
'''

from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
import shutil
import timeit
import random
import datetime
import pathlib
import math
pd.options.mode.chained_assignment = None  # default='warn'
import plotly.graph_objs as go



class CellClass():
	def __init__(self, name, coord_path, coord_cols, tpm_path, lineage, genes):

		self.name = name
		self.lineage = lineage
		self.coord_path = coord_path
		self.coord_data = pd.read_csv(self.coord_path, names = coord_cols, index_col = False, header=None)
		# self.color = list()
		# self.assoc = list()

		self.TPM_means, self.TPM_loess  = self.setTPMFrames(tpm_path, genes)

	def setTPMFrames(self, tpm_path, genes):

		means_frames = list()
		loess_frames = list()

		for gene in genes:
			df = pd.read_csv('{}/{}/{}.csv'.format(tpm_path, gene, self.name))
			df['gene'] = gene
			#df['name'] = self.name
			temp_m = df.loc[df['data.type'] == 'means']
			temp_l = df.loc[df['data.type'] == 'loess']

			temp_l['y'].clip(lower = 0, inplace = True)

			#temp_l = temp_l.loc[temp_l['x'] >= 420] #cutoff at 420
			#Filling early timepoints
			fill_early = list(range(0, temp_l['x'].min()))
			fill_e_df = pd.DataFrame(data = {'x': fill_early, 'gene':gene, 'data.type': 'loess'})
			fill_e_df.reset_index(inplace = True)

			fill_late = list(range(temp_l['x'].max()+1, 900))
			fill_l_df = pd.DataFrame(data = {'x': fill_late, 'gene':gene, 'data.type': 'loess'})
			fill_l_df.reset_index(inplace = True)

			temp_l = pd.concat([fill_e_df, temp_l, fill_l_df])
			temp_l = temp_l.loc[temp_l['x'] >= 420]
			temp_l = temp_l.loc[temp_l['x'] <= 839]
			temp_l.rename(columns = {'x':'time', 'y':'TPM'}, inplace = True)
			temp_l.reset_index(inplace = True)
			#Appending coords
			temp_coord = self.coord_data[['x', 'y', 'z']]
			temp_l = pd.concat([temp_l, temp_coord], axis = 1)

			means_frames.append(temp_m)
			loess_frames.append(temp_l)


		means_df = pd.concat(means_frames)
		loess_df = pd.concat(loess_frames)
		loess_df['norm_loess_by_gene'] = 0
		loess_df = loess_df[['time', 'gene', 'TPM', 'ymin', 'ymax', 'se', 'x', 'y', 'z', 'assoc.factor']]
		loess_df['plot.type'] = 'cell'
		loess_df['color'] = 'lightblue'
		loess_df['name'] = self.name
		return(means_df, loess_df)

class SeamCellClass():
	def __init__(self, name, coord_path, coord_cols, lineage):

		self.name = name
		self.lineage = lineage
		self.coord_path = coord_path
		self.coords = dict()
		self.coord_data = pd.read_csv(self.coord_path, names = coord_cols, index_col = False, header=None)
		self.coord_data['plot.type'] = 'seam cell'
		self.coord_data['color'] = 'lightgreen'
		self.coord_data['name'] = self.name
		self.coord_data['time'] += 420
	#
	#
	# #### Setters ####

def main():
	gstart = timeit.default_timer()
	genes = getGenes(['unc-54'])
	imgDim = [1024, 512]

	gend  = timeit.default_timer()
	print('getGenes()', gend-gstart)


	model_cell_dir = "data/model_cell_coords"
	GSE_cell = pd.read_csv("data/GSE126954/GSE126954_cell_annotation.csv")
	GSE_gene = pd.read_csv("data/GSE126954/GSE126954_gene_annotation.csv")
	masterkey = pd.read_csv("cell keys/masterkey.csv")
	gene_output_dir = "output/{}".format(datetime.date.today())
	#outputsuff = '_'.join(str(e) for e in genes)
	#image_output_dir = gene_output_dir+'/'+outputsuff+'_visualization'

	lstart = timeit.default_timer()
	cells, seamCells = loadCells(model_cell_dir, masterkey, gene_output_dir, genes)
	lend = timeit.default_timer()
	print('loadCells()', lend-lstart)
	#normalize(genes, cells, seamCells)

	plot3Dx(cells, seamCells, genes)
	# plot3DVol(cells, seamCells, genes)
	print(timeit.default_timer())

def plot3D(cells, seamCells, genes):

	plotly_data = list()
	for cell in cells: 
		plotly_data.append(cell.TPM_loess)
	for cell in seamCells: 
		plotly_data.append(cell.coord_data)

	plotly_data = pd.concat(plotly_data)

	#First trace
	tracedata = plotly_data[plotly_data['time'] == 420]
	#print(tracedata)
	trace = go.Scatter3d(
		x = tracedata['x'],
		y = tracedata['y'],
		z = tracedata['z'],
		mode = 'markers',
		marker = dict(size = 9, 
					  colorscale = 'Viridis',
					  color = plotly_data['RGB']
					  )
		)
	#wormLayout = go.Layout(title = 'Creative title here', scene = dict(aspectmode = 'data'))
	fig = go.Figure(data = [trace])

	for timepoint in range(421,839):
		tracedata = plotly_data[plotly_data['time'] == timepoint]

		fig.add_trace(
			go.Scatter3d(
						visible = False,
						x = tracedata['x'],
						y = tracedata['y'],
						z = tracedata['z'],
						mode = 'markers',
						marker = dict(size = 9, 
									  colorscale = 'Viridis',
									  color = plotly_data['RGB']
						)
			)
		)
	fig.data[0].visible = True
	steps = []
	for i in range(len(fig.data)): 
		step = dict(
			method = 'update',
			args = [{'visible': [False] * len(fig.data)},
					{'title': 'Minutes post fertilization: ' +str(i)}]

		)
		step['args'][0]['visible'][i] = True # Changes this step to be visible
		steps.append(step)



	sliders = [dict(
		active = 0,
		currentvalue = {"prefix": "Time: "},
		pad = {'t':1}, 
		steps = steps
	)]

	fig.update_layout(sliders = sliders)



	camera = dict(
	    up=dict(x=1, y=0, z=0),
	    center=dict(x=0, y=0, z=0),
	    eye=dict(x=0, y=2.5, z=0)
	)
	fig.update_layout(scene_camera=camera)

	fig.update_layout(scene = dict(aspectmode = 'data'))


	fig.show()

def plot3Dx(cells, seamCells, genes): 
	import plotly.express as px

	plotly_data = list()
	for cell in cells: 
		plotly_data.append(cell.TPM_loess)
	for cell in seamCells: 
		plotly_data.append(cell.coord_data)

	plotly_data = pd.concat(plotly_data)
	range_x = [plotly_data['x'].min(), plotly_data['x'].max()]
	range_y = [plotly_data['y'].min(), plotly_data['y'].max()]
	range_z = [plotly_data['z'].min(), plotly_data['z'].max()]
	height = abs(plotly_data['y'].min()) + abs(plotly_data['y'].max())
	width = abs(plotly_data['z'].min()) + abs(plotly_data['z'].max())


	fig = px.scatter_3d(plotly_data,
					   x = 'x',
					   y = 'y',
					   z='z',
					   title = 'Post-twitching expression of {}'.format(genes[0]),
					   animation_frame = 'time',
					   animation_group = 'plot.type',
					   color = 'TPM',
					   hover_name = 'name',
					   color_continuous_scale = ['darkred', 
					   							 'orangered', 
					   							 'orange', 
					   							 'yellow', 
					   							 'lightyellow'],

					   range_color = (plotly_data['TPM'].min(), plotly_data['TPM'].max()),
					   )
	camera = dict(
	    up=dict(x=1, y=0, z=0),
	    center=dict(x=0, y=0, z=0),
	    eye=dict(x=0, y=4, z=0)
	)
	fig.update_layout(scene_camera=camera)
	fig.update_layout(scene = dict(aspectmode = 'data'))
	fig.update

	# fig.show()

	import plotly.io as pio
	pio.write_html(fig, file='index.html', auto_open=True)

def plot3DVol(cells, seamCells, genes):
	plotly_data = list()
	for cell in cells: 
		plotly_data.append(cell.TPM_loess)
	for cell in seamCells: 
		plotly_data.append(cell.coord_data)

	plotly_data = pd.concat(plotly_data)

	#First trace
	tracedata = plotly_data[plotly_data['time'] == 420]
	#print(tracedata)
	trace = go.Volume(
		x = tracedata['x'],
		y = tracedata['y'],
		z = tracedata['z'],
		value = tracedata['TPM'],
		isomin = 0.1,
		isomax = 0.8,
		opacity = 0.1,
		surface_count = 17)
	#wormLayout = go.Layout(title = 'Creative title here', scene = dict(aspectmode = 'data'))
	fig = go.Figure(data = [trace])


	fig.show()

def normalize(genes, cells, seamCells):

	'''
	double normalization:

	1) Normalize across all cells within their genes. (Cell AVG will have a normalized TPM for both xxx-1 and xxx-2 for all timepoints.)
	2) Across all cells, take the sum of the normalized tpm for both genes. (AVG :: sum( norm(tpm1, tpm2) ) )
	   such that each cell in each timepoint will have one normalized TPM value
	3) Normalize that single summed norm TPM using the maximum sum(norm(tpm)) across all cells and all timepoints 

	'''

	##### S1 #####

	for gene in genes:
		maxgene = list()
		for cell in cells:
			maxgene.append(cell.TPM_loess.loc[cell.TPM_loess['gene'] == gene]['y'].max())

		maxgene = max(maxgene)
		print('maxmax', maxgene)
		for cell in cells:
			mask = (cell.TPM_loess['gene'] == gene)
			matching_cells = cell.TPM_loess[mask]

			cell.TPM_loess.loc[mask, 'norm_loess_by_gene'] = matching_cells['y'] / maxgene

	for cell in cells: 
		cell.TPM_loess['RGB'] = cell.TPM_loess.apply(lambda x: fillColors(x['norm_loess_by_gene']), axis = 1)

	for cell in seamCells: 
		cell.coord_data['RGB']= [(0,128,0)] * len(cell.coord_data)

def fillColors(norm_val):

	# intensity = int(norm_val * (255*3))

	# if math.isnan(assoc) == True: 
	# 	return 128, 128, 128

	# if intensity > 255*2:
	# 	#rgb = ((255*3)-intensity, 0, 0)
	# 	R = 255*3 - intensity
	# 	G = 0
	# 	B = 0
	# elif intensity > 255:
	# 	#rgb = (255,(255*2)-intensity, 0)
	# 	R = 255
	# 	G = 255*2 - intensity
	# 	B = 0
	# else:
	# 	#less than 255
	# 	#rgb = (255,255,255-intensity)
	# 	R = 255
	# 	G = 255 
	# 	B = 255 - intensity
	# return R, G, B

	intensity = int(norm_val * (255*3))

	if intensity > 255*2:
		rgb = ((255*3)-intensity, 0, 0)
	elif intensity > 255:
		# pass
		rgb = (255,(255*2)-intensity, 0)
	else:
		#less than 255
		rgb = (255,255,255-intensity)
	return rgb

def filter(genes, cells):
	final_cells = list()
	missing_ls = list()
	for cell in cells:
		ct = len(genes)
		for gene in genes:
			gframe = cell.TPM_loess.loc[cell.TPM_loess['gene'] == gene]
			if len(cell.TPM_means[cell.TPM_means['gene'] == gene]) < 20:
				missing_ls.append('{}'.format(cell.name))
				ct -= 1
				break
			elif gframe['se'].max() > cell.TPM_means.loc[cell.TPM_means['gene'] == gene]['y'].max():
				missing_ls.append('{}'.format(cell.name))
				ct -= 1
				break
		if len(genes) == ct:
			final_cells.append(cell)
	print("Following cells [{}] will be dropped due to insufficient data: \n{}".format(int(len(missing_ls)), '\n'.join(missing_ls)))

	return(final_cells)

def getGenes(genein = None):
	if genein == None:
		print("Enter gene name(s) below separated by commas.\nEx: 'par-1, par-2, par-3' ")

		genein = input("\nGenes: ").lower().replace(" ", "")
		genesls = genein.strip().split(',')

		return(genesls)
	else:
		return(genein)

def loadCells(model_cell_dir, masterkey, gene_output_dir, genes):

	sc = [
			"H0L", "H1L", "H2L", "V1L", "V2L", "V3L", "V4L", "QL", "V5L", "V6L", "TL",
			"H0R", "H1R", "H2R", "V1R", "V2R", "V3R", "V4R", "QR", "V5R", "V6R", "TR"
		 ]

	model_cell_names = masterkey['model cellname'].unique()

	cells = list()
	seamCells = list()
	missing_ls = list()
	final_model_cell_ls = list()
	for name in model_cell_names:
		ct = 0
		path = '{}/{}/{}.csv'.format(gene_output_dir, genes[0], name)
		if os.path.exists(path) == False:
			missing_ls.append("{}".format(name))
			ct += 1

		if ct == 0:
			final_model_cell_ls.append(name)

	print("Following cells [{}] will be dropped due to insufficient data: \n{}".format(int(len(missing_ls)), '\n'.join(missing_ls)))

	coord_cols = ['time', 'x', 'y', 'z', 'fill', 'R', 'G', 'B']

	for cellname in final_model_cell_ls:
		wa_lin = masterkey[masterkey['model cellname'] == cellname]['wormatlas lineage'].to_list()
		wa_lin = wa_lin[0]
		coord_path = model_cell_dir+'/{}.csv'.format(cellname)

		if cellname in sc:
			seamCells.append(SeamCellClass(name = cellname, coord_path = coord_path, coord_cols = coord_cols, lineage = wa_lin))
		elif cellname in model_cell_names:
			cells.append(CellClass(name = cellname, coord_path = coord_path, coord_cols = coord_cols, tpm_path = gene_output_dir, lineage = wa_lin, genes = genes))
		else:
			print("{} did not load properly. ".format(cellname))

	return cells, seamCells


main()
