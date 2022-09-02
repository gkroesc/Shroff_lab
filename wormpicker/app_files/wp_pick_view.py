'''
Module for viewing strains in current database
'''

#from os import path 
#import tkinter as tk
from tkinter import ttk
#import datetime
from pandastable import Table
#import csv
#import pandas as pd 
#from tkcalendar import DateEntry
#from ttkthemes import ThemedStyle

##################################################

class Create(ttk.Frame):
	'''
	Window created by controller window and anchored in notebook frame
	Purpose: Give user an interface to view and edit preveiously 
	added strains in the database. 
	Uses Pandas Table module, allowing for intuitive interaction with dataframe objects
	'''
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)

		self.parent = parent 
		self.controller = controller
		self.Page2Frame = ttk.Frame(self.parent)
		self.Page2Frame.grid()
		self.Page2Frame.grid_columnconfigure(0, weight=1)
		self.parent.add(self.Page2Frame, text = 'View database strains') #Add tab to NB

		self.dataWin = DataView(self.Page2Frame, self.controller)
 
class DataView(ttk.Frame):
	''' 
	Class called by page 2 class that uses PandasTable
	to map data to an interactive table visualization
	uses getData class from main controller window.
	Data is limited on what is passed through by getData.
	'''
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.controller = controller
		self.parent = parent
		self.viewWindow = ttk.Frame(self.parent)
		#self.viewWindow.grid(sticky='nesw')
		#self.viewWindow.grid_columnconfigure(0, weight=1)
		self.viewWindow.pack(fill = 'both', expand=True)
		self.df = self.controller.getData() 
		#print('DataView:', id(self.df), type(self.df))

		self.table = self.pt = Table(self.viewWindow, dataframe = self.df)
		self.pt.show()


	def refresh(self): #To fully refresh, the csv would need to be saved, closed, then opened again and
						# loaded into the table via self.pt.model.df = pd.read_csv('WormStrainsData.csv')
						# Then redrawn again. Shouldn't really be necessary unless multiple users at same time. 
		self.pt.redraw()