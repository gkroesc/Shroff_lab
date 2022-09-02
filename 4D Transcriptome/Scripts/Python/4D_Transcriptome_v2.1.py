
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



# print [name for name in os.listdir(".") if os.path.isdir(name)]


class CellClass():
	def __init__(self, name, coord_path, coord_cols, tpm_path, lineage, genes):
		pass


class SeamCellClass():
	def __init__(self, name, coord_path, coord_cols, lineage):
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
	'''
	1. Load all the cells for all the genes (might as well right?) 
	2. Get the genes in the directory for today? 
		- ask which genes of {} you'd like to visualize
		- ask if youd like to vidualize all
	3. for both single and multiple gene loading, <- what if a subsection of pathway? 
	   	- CellClass will have a coord_data file, which holds the coordinates from the worm atlas. 
	   	- It will also have two large csvs containing all gene expression in both 
	   	  mean form and loess form. 
	   	- At beginning of visualization, copy of coord_data created for each cell.
	   	- this copy will serve as the actual data file for the analysis.
	   		- Data will not be appended to it until the very end after normalization. 
	   		- essentially only RGB data should go into the coord_data
	   	- if multiple genes, double normalization
	   	- if single gene, single normalization to 0-1.

	'''

	#get genes in path
	all_gene_ex_path = 'output/{}'.format(datetime.date.today())
	model_cell_dir = "data/model_cell_coords"
	GSE_cell = pd.read_csv("data/GSE126954/GSE126954_cell_annotation.csv")
	GSE_gene = pd.read_csv("data/GSE126954/GSE126954_gene_annotation.csv")
	masterkey = pd.read_csv("cell keys/masterkey.csv")









	#print(all_gene_ex_path)
	#print()
	genes = os.listdir(os.getcwd()+'/'+all_gene_ex_path)

	print("Genes in directory: {}".format(', '.join(genes)))
	loadCells(genes, masterkey, all_gene_ex_path, cell_coord_path = model_cell_dir)

def loadCells(genes, masterkey, all_gene_ex_path, cell_coord_path):
	sc = ["H0L", "H1L", "H2L", "V1L", "V2L", "V3L", "V4L", "QL", "V5L", "V6L", "TL",
			"H0R", "H1R", "H2R", "V1R", "V2R", "V3R", "V4R", "QR", "V5R", "V6R", "TR"]
	coord_cols = ['time', 'x', 'y', 'z', 'fill', 'R', 'G', 'B']

	model_cells = masterkey['model cellname'].unique()

	cells = list()
	seamCells = list()
	missing_ls = list()
	final_model_cell_ls = list()

	for cell in model_cells:
		wa_lin = masterkey[masterkey['model cellname'] == cell]['wormatlas lineage'].to_list()[0]
		if cell in sc:
			seamCells.append(SeamCellClass(name = cell,
			 							   coord_path = cell_coord_path+'/{}.csv'.format(cell),
			   							   coord_cols = coord_cols,
			   							   lineage = wa_lin))
			continue
		missing = 0 
		for gene in genes:
			path = '{}/{}.csv'.format(all_gene_ex_path, gene, cell)
			print(path)
			if os.path.exists(path) == False: 
				missing_ls.append(cell)
				missing += 1
				break
		if missing != 0:
			final_model_cell_ls.append(cell)
		else:
			cells.append(CellClass(name = cell, 
								   coord_path = cell_coord_path+'/{}.csv'.format(cell), 
								   coord_cols = coord_cols, 
								   tpm_path = gene_output_dir, 
								   lineage = wa_lin, 
								   genes = genes))


	print("Following {} cells will be dropped due to insufficient data: \n{}".format(int(len(missing_ls)), '\n'.join(missing_ls)))


	return cells, seamCells





main()