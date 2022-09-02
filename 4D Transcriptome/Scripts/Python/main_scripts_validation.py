'''

4D Transcriptome

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


class SeamCellClass():
	def __init__(self, name, coord_path, tpm_path, lineage):

		self.name = name
		self.lineage = lineage
		self.coord_path = coord_path
		self.tpm_path = tpm_path
		self.coords = dict()
		self.coord_data = pd.read_csv(self.coord_path, index_col = False, header=None)
		self.color = (0,255,0)
		self.mmidx = dict()
		self.coords["x"] = list()
		self.coords["y"] = list()
		self.coords["z"] = list()



	#### Setters ####
	def setCoords(self):
		for i in range(len(self.coord_data)):
			self.coords["x"].append(self.coord_data.iat[i,1])
			self.coords["y"].append(self.coord_data.iat[i,2])
			self.coords["z"].append(self.coord_data.iat[i,3])


	#### Getters ####
	def getCoords(self):
		print("Number of coordinates --> x: {}, y: {}, z: {}".format(self.coords["x"], self.coords["y"], self.coords["z"]))

	def getTPM(self, time):
		pass

class CellClass():
	def __init__(self, name, coord_path, tpm_path, lineage):

		self.name = name
		self.lineage = lineage
		self.coord_path = coord_path
		self.tpm_path = tpm_path
		self.coords = dict()
		self.coord_data = pd.read_csv(self.coord_path, index_col = False, header=None)
		self.color = list()
		self.assoc = list()
		self.coords["x"] = list()
		self.coords["y"] = list()
		self.coords["z"] = list()



	#### Setters ####
	def setCoords(self):
		for i in range(len(self.coord_data)):
			self.coords["x"].append(self.coord_data.iat[i,1])
			self.coords["y"].append(self.coord_data.iat[i,2])
			self.coords["z"].append(self.coord_data.iat[i,3])


	def setTPM(self):
		try:
			self.tpm_csv = pd.read_csv(self.tpm_path+"/"+self.name+".csv")
		except FileNotFoundError: #File does not exist because not enough data exists to create a loess curve reliably
			self.smooth_data = pd.DataFrame()
			return
		timeconstant = 45 #Difference between minutes post fertilization and post first cleavage

		self.smooth_data = self.tpm_csv[self.tpm_csv['data.type'] == "loess"]
		#smooth_data only contains data after 420 (twitching)
		self.smooth_data = self.smooth_data[self.smooth_data['x'] >= 420-timeconstant]
		#Keeping raw data for?
		self.raw_data = self.tpm_csv[self.tpm_csv['data.type'] == "means"]

		# Align times
		self.smooth_data['x'] = self.smooth_data['x'] + 45

		if len(self.smooth_data) == 0:
			self.smooth_data = pd.DataFrame()
			return

		#Negative --> 0
		#self.smooth_data['y'][self.smooth_data['y'] < 0] = 0
		self.smooth_data.loc[self.smooth_data['y']<0,'y']=0

		#If current data is empty --> There are no timepoints greater than or equal to 420. Discard

		#If current data starts later than 420, add empty timepoints to beginning
		if self.smooth_data['x'].min() > 420:
			pre_diff = self.smooth_data['x'].min() - 420
			fillx = list()
			for i in range(int(pre_diff)):
				fillx.append(420+i)
			fill_df = {'x':fillx}

			fill_df = pd.DataFrame(data = fill_df)
			self.smooth_data = pd.concat([fill_df, self.smooth_data])


		#If current data does not reach until the end of twitching
		if self.smooth_data['x'].max() < 840:

			last = self.smooth_data['x'].max()
			post_diff = 840 - last
			fillx = list()
			for i in range(1,int(post_diff)):
				fillx.append(last+i)

			fill_df = {'x':fillx}
			fill_df = pd.DataFrame(data = fill_df)

			self.smooth_data = pd.concat([self.smooth_data, fill_df])

		return


	def setColor(self, maxnorm, minnorm):

		self.color = list()
		#LOW -----------------------------------> HIGH
		#WHITE ----->  YELLOW ----->  RED -----> BLACK
		#(255,255,255),(255,255,0), (255,0,0), 	(0,0,0)

		if self.smooth_data.empty == True:
			for tpm in range(len(self.coords['x'])):
				rgb = (128,128,128)
				self.color.append(rgb)
				self.assoc.append(0)
			return
		for tpm in self.smooth_data['y'].to_list():
			if math.isnan(tpm):
				rgb = (128,128,128)
			else:
				norm_tpm = (tpm-minnorm) / (maxnorm-minnorm) #norm tpm 0 < x < 1
				intensity = int(norm_tpm * (255*3))

				if intensity > 255*2:
					rgb = ((255*3)-intensity, 0, 0)
				elif intensity > 255:
					pass
					rgb = (255,(255*2)-intensity, 0)
				else:
					#less than 255
					rgb = (255,255,255-intensity)
			self.color.append(rgb)

		for ass in self.smooth_data['assoc.factor'].to_list():
			if math.isnan(ass):
				self.assoc.append(0)
			else:
				self.assoc.append(ass)
		'''

		#norm = (x - min(x)) / (max(x) - min(x))
		if self.smooth_data.empty == True:
			for tpm in range(len(self.coords['x'])):
				rgb = (128,128,128)
				self.color.append(rgb)
				self.assoc.append(0)
			return
		for tpm in self.smooth_data['y'].to_list():
			if math.isnan(tpm):
				rgb = (128,128,128)
			else:
				norm_tpm = (tpm-minnorm) / (maxnorm-minnorm) #norm tpm 0 < x < 1
				intensity = norm_tpm * (255*2 + (255-128))  #maxcolor = dark red, min color = white
				if intensity == "nan":
					rgb = (128,128,128)

				elif intensity > (255+255):
					rgb = ( int(intensity)-(255*2), 0, 0) #Dark red to red

				elif intensity < (255+255) and intensity > (255):
					rgb = (255, int(intensity)-255, 0) #Red to yellow

				elif intensity < 255:
					rgb = (255, 255, int(intensity)) #yellow to white
		'''




	#### Getters ####
	def getCoords(self):
		print("Number of coordinates --> x: {}, y: {}, z: {}".format(self.coords["x"], self.coords["y"], self.coords["z"]))


	def getTPM(self, time):
		pass

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
	### PATHS ###
	model_cell_dir = "data/model_cell_coords"
	GSE_cell = pd.read_csv("data/GSE126954_cell_annotation.csv")
	GSE_gene = pd.read_csv("data/GSE126954_gene_annotation.csv")
	gene = getGene(GSE_gene)

	masterkey = pd.read_csv("cell keys/masterkey.csv")
	packer_s6 = pd.read_csv("cell keys/packer_s6.csv")
	start = timeit.default_timer()

	#gene = 'emb-9'
	smooth_gene_output = "output/{}/{}".format(datetime.date.today(), gene)
	image_output_dir = smooth_gene_output+'/validation_visualization'
	pathlib.Path(image_output_dir).mkdir(parents=True, exist_ok=True)


	### Instantiate cell classes ###
	cells, seamCells = loadCells(model_cell_dir, masterkey, smooth_gene_output)

	### Set coordinates ###
	imgDim = [512, 1024]

	mainCoords(cells, seamCells)
	maxmax, minmin = mainColor(cells, seamCells)

	mainDraw(gene, cells, seamCells, imgDim, image_output_dir, maxmax, minmin)
	stop = timeit.default_timer()
	print("Time elapsed: {}s".format(stop-start))

	#for color in cells[1].color: print(cells[1].name, color)
	#for cell in cells:
	#	print(cell.name, cells.index(cell))

def getGene(GSE_gene):
	#Check 6/14/22
	'''
	uses input to collect gene name. Must be a gene present in the data. As of 6/23,
	only genes that have been analyzed manually through R may be used
	'''
	while True:

		genename = input("Enter gene of interest: ")
		if genename in GSE_gene['gene_short_name'].unique():
			break
		else:
			print("\n{} is not a valid gene in GSE126954_gene_annotation.csv\nPlease try again.")

	return genename

def loadCells(model_cell_dir, masterkey, tpm_path):
	#Check 6/14/22
	'''
	input: directory for cells in model, masterkey, path for calculated TPM (from R)
	purpose: initiate classes for each cell. seam cells and tracked cells.
	output: list of seam cells and list of cells. Each cell can be called by indexing the list and using class operators
	'''
	sc = ["H0L", "H1L", "H2L", "V1L", "V2L", "V3L", "V4L", "QL", "V5L", "V6L", "TL",
			"H0R", "H1R", "H2R", "V1R", "V2R", "V3R", "V4R", "QR", "V5R", "V6R", "TR"]

	model_cell_names = masterkey['model cellname'].unique()

	cells = []
	seamCells = []
	#getting coords
	for cellname in model_cell_names:
		wa_lin = masterkey[masterkey['model cellname'] == cellname]['wormatlas lineage'].to_list()
		wa_lin = wa_lin[0]
		coord_path = model_cell_dir+'/{}.csv'.format(cellname)


		if cellname in sc:
			seamCells.append(SeamCellClass(name = cellname, coord_path = coord_path, tpm_path = tpm_path, lineage = wa_lin))
		elif cellname in model_cell_names:
			cells.append(CellClass(name = cellname, coord_path = coord_path, tpm_path = tpm_path, lineage = wa_lin))
		else:
			noAnnls += 1

	return cells, seamCells

def mainCoords(cells, seamCells):
	#Check 6/14/22
	'''
	sets coordinated for each cell/seamcell
	uses class functions

	'''
	for cell in cells:
		cell.setCoords()
	for cell in seamCells:
		cell.setCoords()

def mainColor(cells, seamCells):
	#check 6/14/22
	'''
	gets the range of TPM (min and max) and uses it to normalize data to 255
	min and max are passed through cells' setcolor() to set color for timepoint
	'''
	maxls = list()
	minls = list()

	for cell in cells:
		cell.setTPM()
	ct = 0
	ctls = []
	for cell in cells:
		if cell.smooth_data.empty == True:
			ct += 1
			ctls.append(cell.name)
			continue
		else:
			#print(cell.name)
			#cell.smooth_data.drop(cell.smooth_data['y'].idxmax(), inplace=True)
			#print(cell.smooth_data)
			maxls.append(max(cell.smooth_data['y'].dropna()))
			minls.append(min(cell.smooth_data['y'].dropna()))
	maxmax = max(maxls)
	minmin = min(minls)
	print('Max TPM:',maxmax)
	print('Min TPM:',minmin)
	print("{} out of the {} accounted-for cells in the model do not have enough data.".format(ct, len(cells)+len(seamCells)))
	for x in ctls: print(x)

	for cell in cells:
		cell.setColor(maxmax, minmin)

	return maxmax, minmin

def mainDraw(genename, cells, seamCells, imgDim, outputdir, max_TPM, min_TPM, radius = 5, bgcolor = (100,100,255)):
	#check 6/14/22
	'''
	overall function caller for drawing functions
	'''
	scaleFactor = 4.75
	if os.path.exists(outputdir):
		shutil.rmtree(outputdir)
	os.makedirs(outputdir)
	#for t in range(50):
	validation_cell = input("Enter cellname for validation: ")

	for t in range(len(cells[0].coords["x"])):
		img = Image.new(mode = "RGB", size = (imgDim),
					color = bgcolor)
		draw = ImageDraw.Draw(img)
		drawCellCircle(draw, seamCells, cells, imgDim, scaleFactor, radius, t, validation_cell)
		drawOutline(draw, seamCells, imgDim, scaleFactor, radius, t)
		drawWords("Gene: {}\n\nTime: {} m.p.f.".format(genename, t+420), draw, imgDim)
		drawScaleBar(draw, imgDim, max_TPM, min_TPM, radius)
		img.save("{}/{}.png".format(outputdir, t))
	print("Stack Complete. Saved to {}".format(outputdir))

def drawCellCircle(draw, seamCells, cells, imgDim, scaleFactor, radius, t, validation_cell):
	#check 6/14/22
	'''
	draws circles at specific coordinate for each cell. Using an arbitrary association factor where
	1 < x < 3, circles will be drawn if the association is close or triangles if not.
	closeness or association is based on whether the data point in the scRNAseq has been labelled with
	a cell name and or a lineage.
	'''


	for cell in cells:
		if cell.name != validation_cell:
			continue

		drawWords("TPM: {}\nRGB: {}".format(cell.smooth_data[cell.smooth_data.loc[cell.smooth_data.index[t], 'y']], cell.color))
		if cell.assoc[t] > 2.75:		#Association factor of 3 means that it is a close match (cell=cell, lineage=lineage)
			x1 = cell.coords["x"][t]
			x2 = cell.coords["x"][t]
			y1 = cell.coords["z"][t]
			y2 = cell.coords["z"][t]
			x1 = x1*scaleFactor -radius
			x2 = x2*scaleFactor +radius
			y1 = y1*scaleFactor -radius
			y2 = y2*scaleFactor +radius
			x1 += imgDim[0] / 2
			x2 += imgDim[0] / 2
			y1 += imgDim[0] / 20
			y2 += imgDim[0] / 20
			#print(cell.color)
			draw.ellipse((x1, y1, x2, y2), fill = cell.color[t], outline ='black')

		else: #Anything else has a relatively low association factor where only lineage or name matches. (2 is lineage match)
			x1 = cell.coords["x"][t]
			x2 = cell.coords["x"][t]
			x3 = cell.coords["x"][t]
			x1 = x1*scaleFactor - radius
			x2 = x2*scaleFactor
			x3 = x3*scaleFactor + radius
			x1 += imgDim[0] / 2
			x2 += imgDim[0] / 2
			x3 += imgDim[0] / 2

			y1 = cell.coords["z"][t]
			y2 = cell.coords["z"][t]
			y3 = cell.coords["z"][t]
			y1 = y1*scaleFactor - radius
			y2 = y2*scaleFactor + radius
			y3 = y3*scaleFactor - radius
			y1 += imgDim[0] / 20
			y2 += imgDim[0] / 20
			y3 += imgDim[0] / 20
			draw.polygon([(x1,y1), (x2, y2), (x3,y3)], fill = cell.color[t], outline = 'black')



	for cell in seamCells:
		x1 = cell.coords["x"][t]
		x2 = cell.coords["x"][t]
		y1 = cell.coords["z"][t]
		y2 = cell.coords["z"][t]

		x1 = x1*scaleFactor -radius
		x2 = x2*scaleFactor +radius
		y1 = y1*scaleFactor -radius
		y2 = y2*scaleFactor +radius
		x1 += imgDim[0] / 2
		x2 += imgDim[0] / 2
		y1 += imgDim[0] / 20
		y2 += imgDim[0] / 20
		draw.ellipse((x1, y1, x2, y2), fill = cell.color, outline ='black')

def drawOutline(draw, seamCells, imgDim, scaleFactor, radius, t):
	#check 6/14/22
	'''
	Draws outline of the worm by connecting each seam cell with its preceding seam cell
	can be improved by connecting it to a pseudo head/tail tip.
	'''
	if t < 280:

		scl = [["H0L", "H1L", "H2L", "V1L", "V2L", "V3L", "V4L", "V5L", "V6L", "TL"],
		["H0R", "H1R", "H2R", "V1R", "V2R", "V3R", "V4R", "V5R", "V6R", "TR"]]

	else:
		scl = [["H0L", "H1L", "H2L", "V1L", "V2L", "V3L", "V4L", "QL", "V5L", "V6L", "TL"],
		["H0R", "H1R", "H2R", "V1R", "V2R", "V3R", "V4R", "QR", "V5R", "V6R", "TR"]]


	for x in scl:
		for i in range(len(x)-1):
			idxa = x[i]
			idxb = x[i+1]
			cella = None
			cellb = None
			for cell in seamCells:
				if cell.name == idxa:
					cella = cell.name
					ax = cell.coords["x"][t]*scaleFactor + (imgDim[0] / 2)
					ay = cell.coords["z"][t]*scaleFactor + (imgDim[0] / 20)
				elif cell.name == idxb:
					cellb = cell.name
					bx = cell.coords["x"][t]*scaleFactor + (imgDim[0] / 2)
					by = cell.coords["z"][t]*scaleFactor + (imgDim[0] / 20)
			shape = [(ax, ay), (bx, by)]
			draw.line(shape, fill = cell.color, width = 3)

def drawWords(phrase, draw, imgDim):
	#check 6/14/22
	'''
	general function to write words on images
	'''

	# font = ImageFont.truetype(<font-file>, <font-size>)
	font = ImageFont.truetype('arial.ttf',18)
	# draw.text((x, y),"Sample Text",(r,g,b))
	draw.text((imgDim[0]*0.05, imgDim[1]*0.05),"{}".format(phrase),(256,256,256), font=font)

def drawScaleBar(draw, imgDim, max_TPM, min_TPM, radius):
	'''
	general function to draw a scalebar using a color gradient
	currently rough and can be improved.
	'''
	#Indicate x and y coords for gradient box
	x1 = int(0.1*imgDim[0])
	x2 = int(0.2*imgDim[0])
	y1 = int(0.25*imgDim[1])
	y2 = int(0.75*imgDim[1])

	#shape keys

	#Max and min labels
	mtpm = str(max_TPM).split('.')
	draw.text((x1, y1-15), "{} TPM".format(mtpm[0]+'.'+mtpm[1][:2]))
	draw.text((x1, y2+5), "{} TPM".format(str(min_TPM)))


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




main()
