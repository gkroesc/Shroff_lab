"""
Cell namer by G-Man and Matthew

12/2/2021 11:00 am
"""


import pandas as pd
import os
import numpy as np

def main():
	"""
	Remove the annotations file and insert your own.
	The script will replace your lineaging annotations with 
	the actual names of the cells according to those listed on Worm Atlas.
	The new 'updated annotations' will be added to the workspace file 'Cell_namer' that the python file is located in. 
	"""
	cellKeyMaster = "cellkeyMaster.csv"
	masterDF = pd.read_csv(cellKeyMaster)
	masterDF.dropna(inplace = True)
	masterKey = masterDF.to_numpy()
	
	userAnnotDF = pd.read_csv("annotations.csv")
	userKey = userAnnotDF.to_numpy()
	updateduserKey = userAnnotDF.to_numpy()
	threeNameList = []
	for i, linName in enumerate(userKey[:, 0]):
		for j, name in enumerate(masterKey[:,1]):
			lowlinName = linName.lower().strip()
			namerep = name.replace(" ", "").lower()
			if lowlinName == namerep:
				threeName = masterKey[j,0]
				updateduserKey[i,0] = threeName
				#threeNameList.append(threeName)


	Updated_DF = pd.DataFrame(updateduserKey)

	Updated_DF.to_csv('updated_annotations.csv', header=None, index = None)
	print(updateduserKey)

	



main()