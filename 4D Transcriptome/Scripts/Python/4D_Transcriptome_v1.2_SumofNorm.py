import plotly.express as px



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
			df['name'] = self.name
			temp_m = df.loc[df['data.type'] == 'means']
			temp_l = df.loc[df['data.type'] == 'loess']

			temp_l['y'].clip(lower = 0, inplace = True)

			#temp_l = temp_l.loc[temp_l['x'] >= 420] #cutoff at 420
			#Filling early timepoints
			fill_early = list(range(0, temp_l['x'].min()))
			fill_e_df = pd.DataFrame(data = {'x': fill_early, 'gene':gene, 'data.type': 'loess'})

			fill_late = list(range(temp_l['x'].max()+1, 900))
			fill_l_df = pd.DataFrame(data = {'x': fill_late, 'gene':gene, 'data.type': 'loess'})


			temp_l = pd.concat([fill_e_df, temp_l, fill_l_df])
			temp_l = temp_l.loc[temp_l['x'] >= 420]
			temp_l = temp_l.loc[temp_l['x'] <= 839]
			temp_l.rename(columns = {'x':'time'})

			#Appending coords
			temp_coord = self.coord_data[['x', 'y', 'z']]
			temp_l = pd.concat([temp_l, temp_coord], axis = 1)

			means_frames.append(temp_m)
			loess_frames.append(temp_l)


		means_df = pd.concat(means_frames)
		loess_df = pd.concat(loess_frames)
		loess_df['norm_loess_by_gene'] = 0
		return(means_df, loess_df)



class SeamCellClass():
	def __init__(self, name, coord_path, coord_cols, lineage):

		self.name = name
		self.lineage = lineage
		self.coord_path = coord_path
		self.coords = dict()
		self.coord_data = pd.read_csv(self.coord_path, names = coord_cols, index_col = False, header=None)
	#
	#
	# #### Setters ####

class Point(object):
	def __init__(self, x, y):
		self.x, self.y = x, y

class Rect(object):
	def __init__(self, x1, y1, x2, y2):
		minx, maxx = (x1,x2) if x1 < x2 else (x2,x1)
		miny, maxy = (y1,y2) if y1 < y2 else (y2,y1)
		self.min = Point(minx, miny)
		self.max = Point(maxx, maxy)

	width  = property(lambda self: self.max.x - self.min.x)
	height = property(lambda self: self.max.y - self.min.y)



def main():
	gstart = timeit.default_timer()
	genes = getGenes(['vab-1', 'vab-2', 'cdh-1'])
	imgDim = [1024, 512]

	gend  = timeit.default_timer()
	print('getGenes()', gend-gstart)


	model_cell_dir = "data/model_cell_coords"
	GSE_cell = pd.read_csv("data/GSE126954/GSE126954_cell_annotation.csv")
	GSE_gene = pd.read_csv("data/GSE126954/GSE126954_gene_annotation.csv")
	masterkey = pd.read_csv("cell keys/masterkey.csv")
	gene_output_dir = "output/{}".format(datetime.date.today())
	outputsuff = '_'.join(str(e) for e in genes)
	image_output_dir = gene_output_dir+'/'+outputsuff+'_visualization'

	lstart = timeit.default_timer()
	cells, seamCells = loadCells(model_cell_dir, masterkey, gene_output_dir, genes)
	lend = timeit.default_timer()
	print('loadCells()', lend-lstart)

	nstart = timeit.default_timer()
	normalize(genes, cells)
	nend = timeit.default_timer()
	print('normalize()', nend-nstart)



	for i in range(5):
		cell = cells[i]
		print(cell.TPM_loess.head())
		print(cell.TPM_loess.info())
		print(cell.coord_data.head())
		print(cell.coord_data.info())

	dstart = timeit.default_timer()
	#mainDraw(cells, seamCells, image_output_dir, imgDim)

	dend = timeit.default_timer()
	print('mainDraw()', dend-dstart)
	#print(cells[random.randint(0, len(cells))].coord_data.to_string())
	#for cell in seamCells: 
		#print(cell.name)

	#print(seamCells[random.randint(0, len(seamCells))].coord_data.to_string())
	print('Total time:', timeit.default_timer())

	fig = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width',
	              color='species')
	fig.show()

def normalize(genes, cells):

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
		# print('maxmax', maxgene)
		for cell in cells:
			mask = (cell.TPM_loess['gene'] == gene)
			matching_cells = cell.TPM_loess[mask]

			cell.TPM_loess.loc[mask, 'norm_loess_by_gene'] = matching_cells['y'] / maxgene

	##### S2 #####

	maxl = list()
	for cell in cells:
		col_list = list()

		for gene in genes: 
			col = cell.TPM_loess.loc[cell.TPM_loess['gene'] == gene]['norm_loess_by_gene'].copy()
			
			col_list.append(col)
		temp_df = pd.concat(col_list, axis = 1, ignore_index = True)

		col = temp_df.sum(axis = 1)
		cell.coord_data['sum_norm'] = col.to_list()
		maxl.append(max(col))

	for cell in cells: 

		cell.coord_data['norm_sum_norm_tpm'] = (cell.coord_data['sum_norm'] / max(maxl))
		cell.coord_data['association'] = cell.TPM_loess.loc[cell.TPM_loess['gene'] == genes[0]]['assoc.factor'].to_list()
		
def fillColors(norm_val, assoc):

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


	if math.isnan(assoc) == True: 
		return (128, 128, 128)
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

def mainDraw(cells, seamCells, image_output_dir, imgDim, radius = 5, bgcolor = (100,100,255)): 

	for cell in cells: 
		cell.coord_data['RGB'] = cell.coord_data.apply(lambda x: fillColors(x['norm_sum_norm_tpm'], x['association']), axis = 1)

	for cell in seamCells: 
		cell.coord_data['RGB']= [(0,128,0)] * len(cell.coord_data)

	for cell in seamCells: 
		if cell.name == 'TL':
			tail_coord = cell.coord_data['z'].iloc[-1]
		elif cell.name == 'H0L':
			head_coord = cell.coord_data['z'].iloc[-1]
		else: 
			continue

	maxlength = abs(int(tail_coord - head_coord)) 
	print('maxlength', maxlength)
	scaleFactor = (imgDim[0] * 0.6) / maxlength
	scaleFactor = abs(scaleFactor)


	#pathlib.Path(image_output_dir).mkdir(parents=True, exist_ok=True)
	if os.path.exists(image_output_dir):
		shutil.rmtree(image_output_dir)
		os.makedirs(image_output_dir)
	for t in range(0, len(cells[0].coord_data["x"])):
		img = Image.new(mode = "RGB", 
						size = (imgDim),
						color = bgcolor)
		
		draw = ImageDraw.Draw(img)
		drawCell(draw, cells, seamCells, imgDim, scaleFactor, radius, t)
		# drawOutline(draw, seamCells, imgDim, scaleFactor, radius, t)
		# drawWords("Gene: {}\n\nTime: {} m.p.f.".format(genename, t+420), draw, imgDim)
		drawScaleBar(draw, imgDim, radius)
		drawKey(draw, imgDim, radius)
		img.save("{}/{}.png".format(image_output_dir, t))
	print("Stack Complete. Saved to {}".format(image_output_dir))

def drawCell(draw, cells, seamCells, imgDim, scaleFactor, radius, t, assoc = True): 
	'''
	Draw cells such that the head points left and the tail points left. 
	Association should be able to be turned on or off. 
	'''


	for cell in seamCells: 

		y1 = cell.coord_data.iat[t, cell.coord_data.columns.get_loc('x')]
		x1 = cell.coord_data.iat[t, cell.coord_data.columns.get_loc('z')]

		y2 = y1
		x2 = x1

		y1 = (y1*scaleFactor) - radius + (imgDim[1] * 0.25)
		y2 = (y2*scaleFactor) + radius + (imgDim[1] * 0.25)
		x1 = (x1*scaleFactor) - radius + (imgDim[0] * 0.1)
		x2 = (x2*scaleFactor) + radius + (imgDim[0] * 0.1)


		draw.ellipse((x1, y1, x2, y2), fill = (0, 255, 0), outline = 'black')
		#print(cell.name, t, "({}, {})".format(x1, y1))


	for cell in cells: 
		y1 = cell.coord_data.iat[t, cell.coord_data.columns.get_loc('x')]
		x1 = cell.coord_data.iat[t, cell.coord_data.columns.get_loc('z')]

		y2 = y1
		x2 = x1

		y1 = (y1*scaleFactor) - radius + (imgDim[1] * 0.25)
		y2 = (y2*scaleFactor) + radius + (imgDim[1] * 0.25)
		x1 = (x1*scaleFactor) - radius + (imgDim[0] * 0.1)
		x2 = (x2*scaleFactor) + radius + (imgDim[0] * 0.1)

		fill = cell.coord_data.iat[t, cell.coord_data.columns.get_loc('RGB')]
		draw.ellipse((x1, y1, x2, y2), fill = fill , outline = 'black')
		#print(cell.name, t, "({}, {})".format(x1, y1))
	

def drawScaleBar(draw, imgDim, radius):
	'''
	general function to draw a scalebar using a color gradient
	currently rough and can be improved.
	'''
	#Indicate x and y coords for gradient box
	x1 = int(0.025*imgDim[0])
	x2 = int(0.05*imgDim[0])
	y1 = int(0.10*imgDim[1])
	y2 = int(0.90*imgDim[1])

	#shape keys

	#Max and min labels
	draw.text((x1, y1-10), "100%") #-30 for two lines, -5 for one line
	draw.text((x1, y2+5), "0%")
	caption = 'Scale bar represents the normalized percent of maximum expression across all genes in pathway.'
	draw.text((x1, y2+25), caption)


	# Draw a three color vertical gradient.
	darkRED, RED, YELLOW, WHITE = ((0, 0, 0), (255, 0, 0), (255, 255, 0), (255, 255, 255))
	color_palette = [darkRED, RED, YELLOW, WHITE]
	region = Rect(x1, y1, x2, y2)
	width, height = region.max.x+1, region.max.y+1

	vert_gradient(draw, region, gradient_color, color_palette)

def vert_gradient(draw, rect, color_func, color_palette):
	'''
	copied from some site
	'''

	minval, maxval = 1, len(color_palette)
	delta = maxval - minval
	height = float(rect.height)  # Cache.
	for y in range(rect.min.y, rect.max.y+1):
		f = (y - rect.min.y) / height
		val = minval + f * delta
		color = color_func(minval, maxval, val, color_palette)
		draw.line([(rect.min.x, y), (rect.max.x, y)], fill=color)

def gradient_color(minval, maxval, val, color_palette):
	""" Computes intermediate RGB color of a value in the range of minval
		to maxval (inclusive) based on a color_palette representing the range.
	"""
	max_index = len(color_palette)-1
	delta = maxval - minval
	if delta == 0:
		delta = 1
	v = float(val-minval) / delta * max_index
	i1, i2 = int(v), min(int(v)+1, max_index)
	(r1, g1, b1), (r2, g2, b2) = color_palette[i1], color_palette[i2]
	f = v - i1
	return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1))


def drawKey(draw, imgDim, radius):

	#draw.text((x1, y1-5), "100%") #-30 for two lines, -5 for one line
	#draw.text((x1, y2+5), "0%")
	offset = int(0.025*imgDim[0])

	#grey
	x = 0.075*imgDim[0]
	y = imgDim[1]*0.6
	shape = [(x, y), (x+offset, y+offset)]
	draw.rectangle(shape, fill = (128, 128, 128), outline = 'black')
	draw.text((x+1.5*offset, y), "No expression data for cell")

	#green
	x = 0.075*imgDim[0]
	y = y + offset*1.5
	shape = [(x, y), (x+offset, y+offset)]
	draw.rectangle(shape, fill = (0, 255, 0), outline = 'black')
	draw.text((x+1.5*offset, y), "Seam Cells")
	#triangle

	#circle


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
