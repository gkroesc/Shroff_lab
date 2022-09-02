'''
gene expression to model main

1) run make key 
	input: none
	output: CellKey.csv --> cols: name, lineage, annotation
								: model name, WB lineage name, packer lineage name
2) get gene name

3) run R script

4) assign colors, fill cell classes

5) generate model

6) save model


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


############### CLASSES ##################


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
		self.color = (255,0,0)
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
			self.tpm_csv = pd.read_csv(self.tpm_path+"\\"+self.name+".csv")
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

		#norm = (x - min(x)) / (max(x) - min(x))
		if self.smooth_data.empty == True:
			for tpm in range(len(self.coords['x'])):
				rgb = (128,128,128)
				self.color.append(rgb)
			return
		for tpm in self.smooth_data['y'].to_list():
			if math.isnan(tpm):
				rgb = (128,128,128)
			else:
				norm_tpm = (tpm-minnorm) / (maxnorm-minnorm)
				intensity = norm_tpm*255*2 
				if intensity == "nan":
					rgb = (128,128,128)
				elif intensity <= 255:
					rgb = (int(intensity), 0, 0)
				else:
					rgb = (255, int(intensity)-255, 0)

			self.color.append(rgb)



	#### Getters ####
	def getCoords(self):
		print("Number of coordinates --> x: {}, y: {}, z: {}".format(self.coords["x"], self.coords["y"], self.coords["z"]))


	def getTPM(self, time):
		pass

############### FUNCTIONS ################

### STEP 1: Make cell key ###

def cleanModelLineages(model):

	#Refine model so that the name has no spaces in it
	name_ls = model['name'].to_list()
	lin_ls = model['lineage'].to_list()
	for i in range(len(lin_ls)):
		lin_ls[i] = lin_ls[i].replace(" ", "").strip().upper()
	modelData = {"name": name_ls, "lineage": lin_ls}

	#Refined model_key
	model = pd.DataFrame(modelData)

	return model 

def alignLineages(model, packer):

	annotation = list()

	packer_lins = packer["cell"].to_list()
	packer_anns = packer["annotation_name"].to_list()
	model_lin = model["lineage"].to_list()

	for i in range(len(model_lin)):

		for j in range(len(packer_lins)):

			if model_lin[i].upper() == packer_lins[j].upper():
				annotation.append(packer_anns[j])
				break
			else:
				continue

	na_count = 0
	for value in annotation:
		if str(value) == "nan":
			na_count += 1
	model_num = len(model_lin) - na_count
	perc = (model_num / len(model_lin)) * 100

	print("{} cells are unaccounted for in the dataset. ".format(na_count))
	print("{} out of {} cells in the model are accounted for.\nCoverage = {}%".format(model_num, len(model_lin), str(perc)[:4]))
	model["annotation"] = annotation
	key = model.copy()

	return key

def countAppearances(key, GSE):
	anns = key["annotation"].to_list()
	GSE_names = GSE["plot.cell.type"].to_list()
	GSE_lins = GSE["lineage"].to_list()
	GSE_times = GSE["embryo.time"].to_list()

	model_counts = dict()
	for ann in anns:
		model_counts[ann] = 0
	model_times = dict()
	for ann in anns:
		model_times[ann] = list()

	apps = 0
	for i in range(len(GSE_lins)):
		if str(GSE_lins[i]) == "nan":
			continue
		elif int(GSE_times[i]) < 300:
			continue

		elif (GSE_lins[i] in anns) and str(GSE_names[i]) != "nan":
			if GSE_times[i] in model_times[GSE_lins[i]]:
				continue
			else:
				model_times[GSE_lins[i]].append(GSE_times[i])
				model_counts[GSE_lins[i]] += 1


	return model_counts, model_times
### STEP 2 ###

### STEP 3 ###

### STEP 4 ###

def loadCells(cellDir, sc, CellKey, tpm_path):
	print("Loading Cells ...")
	start = timeit.default_timer()
	noAnnls = 0
	cells = []
	seamCells = []
	allCellFiles = os.listdir(cellDir)

	model_name_ls = CellKey["name"].to_list()
	lineage_name_ls = CellKey["lineage"].to_list()

	for i in range(len(allCellFiles)):
		cellname = allCellFiles[i][:-4]
		fullpath = cellDir+"\\"+allCellFiles[i]

		try:
			idx = model_name_ls.index(cellname)
			lin_name = lineage_name_ls[idx]
		except ValueError:
			print("{} not in list.".format(cellname))

		if cellname in sc:
			seamCells.append(SeamCellClass(name = cellname, coord_path = fullpath, tpm_path = tpm_path, lineage = lin_name))
		elif cellname in model_name_ls:
			cells.append(CellClass(name = cellname, coord_path = fullpath, tpm_path = tpm_path, lineage = lin_name))
		else:
			noAnnls += 1
	
	stop = timeit.default_timer()
	print("Cells with no known annotation: {}".format(noAnnls))
	print("Runtime: {} seconds".format(stop-start))

	return cells, seamCells

def drawCellPoints(draw, seamCells, cells, imgDim, scaleFactor, t):

	start = timeit.default_timer()
	for cell in cells:
		x = cell.coords["x"][t] * scaleFactor + imgDim[0]/2
		y = cell.coords["z"][t] * scaleFactor + imgDim[0]/2

		draw.point((x,y), fill = cell.color[t])
	for cell in seamCells:
		x = cell.coords["x"][t] * scaleFactor + imgDim[0]/2
		y = cell.coords["z"][t] * scaleFactor + imgDim[0]/2
		draw.point((x,y), fill = cell.color[t])

	stop = timeit.default_timer()
	print("[Dot] Runtime: {} seconds".format(stop-start))

def mainColor(cells, seamCells):
	
	maxls = list()
	minls = list()

	for cell in cells:
		cell.setTPM()

	ct = 0
	for i in range(10):
		if cell.smooth_data.empty == True:
			ct += 1 
			continue
		else:

			maxls.append(max(cell.smooth_data['y'].dropna()))
			minls.append(min(cell.smooth_data['y'].dropna()))
	maxmax = max(maxls)
	minmin = min(minls)
	print(maxmax)
	print(minmin)
	print("{} out of the {} accounted-for cells in the model do not have enough data.".format(ct, len(cells)+len(seamCells)))

	for cell in cells:
		cell.setColor(maxmax, minmin)




def drawCellCircle(draw, seamCells, cells, imgDim, scaleFactor, radius, t):
	
	for cell in cells:
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

def mainDraw(genename, cells, seamCells, imgDim, outputdir, radius = 5, bgcolor = (100,100,255), ):

	scaleFactor = 4.75
	if os.path.exists(outputdir):
		shutil.rmtree(outputdir)
	os.makedirs(outputdir)
	#for t in range(50):
	for t in range(len(cells[0].coords["x"])):
		img = Image.new(mode = "RGB", size = (imgDim),
					color = bgcolor)
		draw = ImageDraw.Draw(img)	
		drawCellCircle(draw, seamCells, cells, imgDim, scaleFactor, radius, t)
		drawOutline(draw, seamCells, imgDim, scaleFactor, radius, t)
		drawWords("Gene: {}\n\nTime: {} m.p.f.".format(genename, t+420), draw, imgDim)
		img.save("{}\\{}.png".format(outputdir, t))
	print("Stack Complete. Saved to {}".format(outputdir))

def drawWords(phrase, draw, imgDim):
	# font = ImageFont.truetype(<font-file>, <font-size>)
	font = ImageFont.truetype("calibri.ttf", 18)
	# draw.text((x, y),"Sample Text",(r,g,b))
	draw.text((0, 50),"{}".format(phrase),(0,0,0), font=font)

def mainCoords(cells, seamCells):
	print("Setting coordinates ...")
	start = timeit.default_timer()
	for cell in cells:
		cell.setCoords()
	for cell in seamCells:
		cell.setCoords()

	stop = timeit.default_timer()
	print("Runtime: {} seconds".format(stop-start))

def mainIndices(cells, seamCells, GSE_cells_df):

	gse_t = GSE_cells_df["embryo.time"].to_list()
	gse_lin = GSE_cells_df["lineage"].to_list()

	for i in range(len(gse_lin)):
		lin_name = str(gse_lin[i])
		if lin_name != "nan":
			for cell in cells:
				if cell.lineage == lin_name:
					cell.mmidx[int(gse_t[i])] = i

			for cell in seamCells:
				if cell.lineage == lin_name:
					cell.mmidx[int(gse_t[i])] = i
		else:
			continue
### STEP 5 ###

### STEP 6 ###


def main():
	### PATHS ###
	GSE_cell = pd.read_csv("data\\GSE126954_cell_annotation.csv")
	GSE_gene = pd.read_csv("data\\GSE126954_gene_annotation.csv")

	model_to_lin = pd.read_csv("cellkeys\\model_to_lin.csv")
	packer_s6 = pd.read_csv("cellkeys\\packer_s6.csv")


	### STEP 1 ####################################################################################################################################

	s1Start = timeit.default_timer()
	model = cleanModelLineages(model_to_lin)
	key = alignLineages(model, packer_s6)
	counts, times = countAppearances(key, GSE_cell)
	name_ls = key["name"].to_list()
	annotation_ls = key["annotation"].to_list()

	#for i in range(len(annotation_ls)):
	#	if annotation_ls[i] in counts.keys():
	#		print(name_ls[i], counts[annotation_ls[i]])
	key.to_csv("cellkeys\\CellKey.csv", index=False)
	s1Stop = timeit.default_timer()

	print("Step 1 Runtime: {}s".format(s1Stop-s1Start))


	### STEP 2 ####################################################################################################################################

	s2Start = timeit.default_timer()

	#while True:
	#
	#	genename = input('Enter gene name: ')
	#	if genename in GSE_gene['gene_short_name'].unique():
	#		break
	#	else:
	#		print("\n{} is not a valid gene in GSE126954_gene_annotation.csv\nPlease try again.")
	genename = 'fhod-1'
	s2Stop = timeit.default_timer()
	print("Step 2 Runtime: {}s".format(s2Stop-s2Start))






	### STEP 3 ####################################################################################################################################
	s3Start = timeit.default_timer()

	#RUN R SCRIPT FROM PYTHON

	#files exported to \\output\\smoothed_output\\cellname


	#smooth_gene_output = somefunction()

	smooth_gene_output = os.getcwd()+"\\output\\{}\\{}".format(datetime.date.today(), genename)

	s3Stop = timeit.default_timer()
	print("Step 3 Runtime: {}s".format(s3Stop-s3Start))
	# Cells with fewer than six (6) points are dropped in the r script before CSVs are generated.











	### STEP 4 ####################################################################################################################################

	s4Start = timeit.default_timer()

	cellDir = "data\\Cells"
	sc = ["H0L", "H1L", "H2L", "V1L", "V2L", "V3L", "V4L", "QL", "V5L", "V6L", "TL", 
			"H0R", "H1R", "H2R", "V1R", "V2R", "V3R", "V4R", "QR", "V5R", "V6R", "TR"]

	#path needs to be specified somehow output\\gene\\date

	path = "C:\\Users\\chawmm\\Desktop\\RNAseq Project\\Cell Mapping\\scripts\\gene_ex_to_model\\output\\{}\\{}".format(datetime.date.today(), genename)
	cells, seamCells = loadCells(cellDir, sc, key, path)
	
	
	
	imgDim = [512, 1024]
	outputdir = os.getcwd()+"\\output\\{}\\{}\\visualization".format(datetime.date.today(), genename)
	#os.mkdir(outputdir)
	pathlib.Path(outputdir).mkdir(parents=True, exist_ok=True)




	#mainIndices(cells, seamCells, pd.read_csv(GSE_cells_path))





	#for cell in seamCells:
		#print(cell.name, cell.lineage, cell.mmidx.keys())

	
	mainCoords(cells, seamCells)

	mainColor(cells, seamCells)
	for cell in cells: 
		print("{}: length: {}, color length: {}".format(cell.name, len(cell.smooth_data), len(cell.color)))

	mainDraw(genename, cells, seamCells, imgDim, outputdir)


	s4Stop = timeit.default_timer()
	print("Step 4 Runtime: {}s".format(s4Stop-s4Start))
	
	### STEP 5 ###
	
	s5Start = timeit.default_timer()

	s5Stop = timeit.default_timer()
	print("Step 5 Runtime: {}s".format(s5Stop-s5Start))
	
	### STEP 6 #######################################################################################################################################
	
	s6Start = timeit.default_timer()

	s6Stop = timeit.default_timer()
	print("Step 6 Runtime: {}s".format(s6Stop-s6Start))








	print("Total Runtime: {}".format(timeit.default_timer()))
main()

