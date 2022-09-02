'''
File for creating, writing, and reading experiment data files

1. Function called from exp plan. Could be any experiment type so
	it should be able to determine which experiment type it is and what 
	functions should be activated. 
2. Once experiment type is determined, then correct function should be used 
	for respective experiment. 
		a. Should there be two sets of functions then for reading and writing for each exp?
'''

from os import path 
#import tkinter as tk
#from tkinter import ttk
#import datetime
#from pandastable import Table
#import csv
import pandas as pd 
#import tkcalendar
#from ttkthemes import ThemedStyle


def writeCross(myDict):

	keys = myDict.keys()
	data = myDict.values()

	newdf = pd.DataFrame([data], columns = keys)
	

	if path.exists('app_files\\exp_cross_data.csv'):
		df = pd.read_csv('app_files\\exp_cross_data.csv')
	else:
		df = pd.DataFrame(columns = keys)
		
		df.to_csv('app_files\\exp_cross_data.csv')
	
	df = pd.concat([df, newdf], join = 'inner', ignore_index = True)
	df.to_csv('app_files\\exp_cross_data.csv', index = False)

	


def readCross():
	df = pd.read_csv('app_files\\exp_cross_data.csv')
	df.sort_values(by = 'p0_date', ascending = False, inplace = True)

	return df
