'''
Module for adding new strains to picking db
'''

#from os import path 
import tkinter as tk
from tkinter import ttk
#import datetime
#from pandastable import Table
#import csv
#import pandas as pd 
from tkcalendar import DateEntry
#from ttkthemes import ThemedStyle


####################################################

class Create(ttk.Frame):
	''' 
	Class called by main controller window
	Purpose: Allow user to input strains to database by
	giving any number or combination of attributes as they 
	relate to C. elegans experiments in Shroff Lab.
	'''
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.parent = parent
		self.controller = controller 

		self.addWin = ttk.Frame(self.parent) #Width has no effect
		self.addWin.grid(sticky='nesw')
		self.parent.add(self.addWin, text='Add new strain', sticky='nesw')
		#self.addWin.grid_columnconfigure(0, weight=1)


		self.addBox = ttk.LabelFrame(self.addWin, text='Strain Variables', style = 'Header.TLabelframe')
		self.addBox.grid(column=0, sticky = 'nw', padx=20, pady=5)
		self.addBox.grid_columnconfigure(0, weight=1)
		self.addBox.grid_rowconfigure(7, weight  = 1)

		#self.eventLogFrame = ttk.LabelFrame(self.addWin, text = 'Event Log', style = 'Header.TLabelframe')#, background='cyan')
		#self.eventLogFrame.grid(column = 1, row = 0, sticky = 'nw', pady=5)
		#self.eventLogFrame.grid_columnconfigure(1, weight=1)

		#self.eventLog = tk.Text(self.eventLogFrame, background = self.controller.themeColor)#) #Inside frame
		#self.eventLog.grid(sticky = 'nesw')
		#self.eventLog.grid_columnconfigure(0, weight=1)


		### Variables
		self.strainvar = StrainClass(self.addBox, self.controller, 0) #self.controller is a downstream reference to ControllerWin
		self.typevar = TypeClass(self.addBox, self.controller, 1) 
		self.constructsvar = ConstructsClass(self.addBox, self.controller, 2) 
		self.statusvar = StatusClass(self.addBox, self.controller, 3) 
		self.pickDatevar = PickDateClass(self.addBox, self.controller, 4)
		self.pickEvery =  PickEveryClass(self.addBox, self.controller, 5)
		self.numPlatesvar = NumPlatesClass(self.addBox, self.controller, 6)
		self.locationvar = LocationClass(self.addBox, self.controller, 7)
		self.notesvar = NotesClass(self.addBox, self.controller, 8)
		### Getting
		self.enterButton = ttk.Button(self.addBox, text = 'Enter', width=25, command = (lambda:self.controller.enterData())) 

		self.enterButton.grid(columnspan = 2, row=9, column=0, pady=5, padx=5) 
class StrainClass(ttk.Frame):#var=self.strain
	'''
	Class called by page 1
	Purpose: create entrybox and label for 
	strain name
	'''
	def __init__(self, addBox, controller, addBoxRow):

		ttk.Frame.__init__(self, addBox)
		self.controller = controller
		self.addBox = addBox 

		ttk.Label(self.addBox, text='Strain Name').grid(row = addBoxRow, sticky='w', pady=5)
		self.strain = ttk.Entry(self.addBox)
		self.strain.grid(row=addBoxRow, column=1, sticky='w', padx=5)
class TypeClass(ttk.Frame):#var=self.strainTypeVar
	'''
	Class called by page 1
	Purpose: Create optionmenu for 'strain type' variables
	and label for box
	'''
	def __init__(self, addBox, controller, addBoxRow):

		ttk.Frame.__init__(self, addBox)
		self.controller = controller
		self.addBox = addBox

		
		
		self.No = tk.IntVar()
		self.In = tk.IntVar()
		self.Ar = tk.IntVar()
		self.Hs = tk.IntVar()
		self.Ma = tk.IntVar()

		self.strainTypesDict = {'None': self.No, 'Integrated': self.In, 'Array':self.Ar, 'Heat shock':self.Hs, 'Males':self.Ma}

		ttk.Label(self.addBox, text= 'Type').grid(row = addBoxRow, sticky= 'nw', pady=5)
		self.checkFrame = ttk.Frame(self.addBox)
		self.checkFrame.grid(row=addBoxRow, column = 1, sticky='w', pady=5)

		self.NoCheck = ttk.Checkbutton(self.checkFrame, text = 'None', variable = self.No ).grid(row = 0, sticky='w')
		self.InCheck = ttk.Checkbutton(self.checkFrame, text = 'Integrated', variable = self.In ).grid(row = 1, sticky='w')
		self.ArCheck = ttk.Checkbutton(self.checkFrame, text = 'Array', variable = self.Ar).grid(row = 2, sticky='w')
		self.HsCheck = ttk.Checkbutton(self.checkFrame, text = 'Heat Shock', variable = self.Hs).grid(row =3, sticky='w')
		self.MaCheck = ttk.Checkbutton(self.checkFrame, text = 'Males', variable = self.Ma).grid(row = 4, sticky='w')

		#self.strainTypeVar = tk.StringVar(self.addBox)
		#self.strainTypeVar.set(self.strainTypesls[0]) # default value
		#self.typeMenu = tk.OptionMenu(self.addBox, self.strainTypeVar, *self.strainTypesls)
		#self.typeMenu.grid(row=1, column=1, sticky='w', padx=5)
class ConstructsClass(ttk.Frame):#var=self.constructs
	'''
	Class called by page 1
	Purpose: Create entry box for constructs and labels
	Dependent on user to know and input necessary constructs
	'''
	def __init__(self, addBox, controller, addBoxRow):

		ttk.Frame.__init__(self, addBox)
		self.controller = controller
		self.addBox = addBox

		ttk.Label(self.addBox, text= 'Construct').grid(row= addBoxRow, sticky= 'w', pady=5)
		self.constructs = ttk.Entry(self.addBox) 
		self.constructs.grid(row=addBoxRow, column=1, sticky='w', padx=5)
class StatusClass(ttk.Frame):#var=self.status
	'''
	Class called by page 1
	Purpose: create option menu for 
	experimental statuses and respective labels
	''' 
	def __init__(self, addBox, controller, addBoxRow): 
		ttk.Frame.__init__(self, addBox)
		self.controller = controller
		self.addBox = addBox 

		

		self.No = tk.IntVar()
		self.Ma = tk.IntVar()
		self.Im = tk.IntVar()
		self.St = tk.IntVar()
		self.Sc = tk.IntVar()
		self.Li = tk.IntVar()
		self.Ct = tk.IntVar()

		self.statusDict = {'None':self.No, 'Maintaining':self.Ma, 'Imaged':self.Im, 'Crossing':self.St, 
							'Screening':self.Sc, 'Lineaging':self.Li, 'Current tracking':self.Ct}

		ttk.Label(self.addBox, text= 'Experimental Status').grid(row=addBoxRow, sticky='nw', pady=5)
		self.checkFrame = ttk.Frame(self.addBox)

		self.checkFrame.grid(row = addBoxRow, column = 1, sticky = 'w')
		self.NoCheck = ttk.Checkbutton(self.checkFrame, text = 'None', variable = self.No ).grid(row = 0, sticky='w')
		self.MaCheck = ttk.Checkbutton(self.checkFrame, text = 'Maintaining', variable = self.Ma ).grid(row = 1, sticky='w')
		self.ImCheck = ttk.Checkbutton(self.checkFrame, text = 'Imaged', variable = self.Im ).grid(row = 2, sticky='w')
		self.StCheck = ttk.Checkbutton(self.checkFrame, text = 'Crossing', variable = self.St ).grid(row = 3, sticky='w')
		self.ScCheck = ttk.Checkbutton(self.checkFrame, text = 'Screening', variable = self.Sc ).grid(row = 4, sticky='w')
		self.LiCheck = ttk.Checkbutton(self.checkFrame, text = 'Lineaging', variable = self.Li ).grid(row = 5, sticky='w')
		self.CtCheck = ttk.Checkbutton(self.checkFrame, text = 'Currently tracking', variable = self.Ct ).grid(row = 6, sticky='w')

		
		#self.status = tk.StringVar(self.addBox)
		#self.status.set(self.statusls[0]) # default value
		#self.statusMenu = tk.OptionMenu(self.addBox, self.status, *self.statusls)
		#self.statusMenu.grid(row=3, column=1, sticky='w', padx=5)
class PickDateClass(ttk.Frame):
	'''
	Class created by page 1
	Purpose: Allows user to select the day last picked. 
	Note: Date defaults to today first, then the last date selected 
	for following entries.
	'''
	def __init__(self, addBox, controller, addBoxRow):
		ttk.Frame.__init__(self, addBox)
		self.addBox = addBox
		self.controller = controller 

		self.lastPick = tk.StringVar()

		self.pickLabel = ttk.Label(self.addBox, text = 'Last Day Picked:')
		self.pickLabel.grid(row = addBoxRow, column =0 , sticky = 'w')

		self.date = DateEntry(self.addBox,selectmode='day', textvariable = self.lastPick, date_pattern = 'yyyy-MM-dd')
		self.date.grid(row=addBoxRow,column=1,pady=5, sticky = 'w')
class PickEveryClass(ttk.Frame):
	'''
	Class created by page 1
	Purpose: Allows user to specify how often a given strain must be maintained
	Units: Days
	'''
	def __init__(self, addBox, controller, addBoxRow):
		self.addBox = addBox
		self.controller = controller 
		self.every = tk.StringVar(self.addBox)
		self.everyOptions = []
		for i in range(0,15):
			self.everyOptions.append(int(i))
		self.every.set(self.everyOptions[3])

		ttk.Label(self.addBox, text = 'Maintain every').grid(row =addBoxRow, column = 0, sticky = 'nw', pady=5)
		
		self.pickEveryMiniFrame = ttk.Frame(self.addBox)
		self.pickEveryMiniFrame.grid(row = addBoxRow, column = 1, sticky='nw', pady=5)

		self.everyMenu = ttk.OptionMenu(self.pickEveryMiniFrame, self.every, *self.everyOptions).grid(row=0, column=0,sticky='nw')
		ttk.Label(self.pickEveryMiniFrame, text = 'day(s)').grid(row=0, column = 1, sticky='nw')
class NumPlatesClass(ttk.Frame):
	'''
	Class created by page 1
	Purpose: Allow user to specify nuber of plates that are routinely maintained. 
	'''
	def __init__(self, addBox, controller, addBoxRow):
		self.addBox = addBox
		self.controller = controller 
		self.numPlates = tk.StringVar(self.addBox)
		self.numPlatesOptions = []
		for i in range(0,21):
			self.numPlatesOptions.append(int(i))
		self.numPlates.set(self.numPlatesOptions[1])

		ttk.Label(self.addBox, text = 'Number of Plates').grid(row = addBoxRow, column = 0, sticky = 'nw', pady=5)
		
		self.numPlatesMiniFrame = ttk.Frame(self.addBox)
		self.numPlatesMiniFrame.grid(row = addBoxRow, column = 1, sticky='nw', pady=5)

		self.numPlatesMenu = ttk.OptionMenu(self.numPlatesMiniFrame, self.numPlates, *self.numPlatesOptions).grid(row=0, column=0,sticky='nw')
		ttk.Label(self.numPlatesMiniFrame, text = 'plate(s)').grid(row=0, column = 1, sticky='nw')
class LocationClass(ttk.Frame):
	def __init__(self, addBox, controller, addBoxRow): #addBox == parent
		ttk.Frame.__init__(self, addBox)
		self.controller = controller
		self.addBox = addBox
		ttk.Label(self.addBox, text = 'Location').grid(row=addBoxRow, sticky='w', pady=5)
		self.location = ttk.Entry(self.addBox)
		self.location.grid(row=addBoxRow, column=1, sticky='w', padx=5)
class NotesClass(ttk.Frame): #var=self.notes
	'''
	Class created by page 1
	Purpose: Allows user to list notes about the strain.
	'''
	def __init__(self, addBox, controller, addBoxRow): #addBox == parent
		ttk.Frame.__init__(self, addBox)
		self.controller = controller
		self.addBox = addBox
		ttk.Label(self.addBox, text = 'Notes').grid(row=addBoxRow, sticky='w', pady=5)
		self.notes = ttk.Entry(self.addBox)
		self.notes.grid(row=addBoxRow, column=1, sticky='w', padx=5)