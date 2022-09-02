"""
Worm picker v3

01/24/22
Utilize modified model-view-controller framework

view-controller

use classes

Icon Created with BioRender.com
"""

import timeit
gstart = timeit.default_timer()
from os import path 
import tkinter as tk
from tkinter import ttk
import datetime
#from pandastable import Table
import csv
import pandas as pd 
#from tkcalendar import DateEntry
from ttkthemes import ThemedStyle

import sys 
sys.path.insert(0, 'app_files')
import wp_pick_add as addpage
import wp_pick_view as viewpage
import wp_pick_todo as todopage 
import wp_exp_plan as planpage

gstop = timeit.default_timer()

print('Inits:',(gstop-gstart))





### PAGE 3: To-Do ###


###### MENU BAR ########

class MenuBar():
	'''
	Menu bar appears at the top of window.
	Options given are: ABOUT, SAVE, REFRESH, EXIT
	'''
	def __init__(self, parent, controller):

		self.parent = parent 
		self.controller = controller 
		self.menubar = tk.Menu(parent)

		self.fileMenu = tk.Menu(self.menubar, tearoff = 0)
		self.helpMenu = tk.Menu(self.menubar, tearoff = 0)
		self.howToMenu = tk.Menu(self.helpMenu, tearoff = 0)

		self.menubar.add_cascade(label = 'File', menu = self.fileMenu)
		self.menubar.add_cascade(label = 'Help', menu = self.helpMenu)

		
		self.fileMenu.add_command(label = 'Save Database', command = lambda:self.SaveDBComm())
		self.fileMenu.add_command(label = 'Refresh', command = lambda:self.RefreshComm())
		self.fileMenu.add_separator()
		self.fileMenu.add_command(label = 'Exit', command = lambda:self.ExitComm())

		self.helpMenu.add_command(label = 'About', command = lambda:self.AboutComm())
		self.helpMenu.add_cascade(label = 'How to', menu = self.howToMenu)

		self.howToMenu.add_command(label = 'Add Strains', command = lambda: self.addHowTo())
		self.howToMenu.add_command(label = 'View and Edit Strains', command = lambda: self.viewHowTo())
		self.howToMenu.add_command(label = 'View To-Do List', command = lambda: self.toDoHowTo())

		self.parent.config(menu = self.menubar)

	def AboutComm(self):
		tk.messagebox.showinfo('Worm Picker', 'Worm Picker is a fun program.')

	def addHowTo(self):
		msg = ('Type strain information into each textbox and make corresponding selections for attributes such as construct or'+
				'intended location.\nWhen ready, click Enter to input the information into the database.')
		tk.messagebox.showinfo('Worm Picker',msg)
	def viewHowTo(self):
		msg = ('Use the view database tab to see all strains. This tab works similar to an excel file in that pre-existing cells can be changed or mutated.'+
				'\nThough be sure to save your work using the save button in Menu --> File --> Save Database') 
		tk.messagebox.showinfo('Worm Picker', msg)
	def toDoHowTo(self):
		msg = ('If a strain is ready to be picked, it wil show up in the to-do list tab along with any other data about it. Strains are deemed ready to be picked when' +
				'the time since the strain was last picked has surpassed the picking frequency. Use the buttons to clear a strain from the list.'+
				'\nMarking as picked will reset the days since picked while snooze will specify a number of days until you are again reminded.') 
		tk.messagebox.showinfo('Worm Picker', msg)
	
	def SaveDBComm(self):
		self.controller.saveDatabase()
		tk.messagebox.showinfo('Worm Picker', 'Data Saved!')

	def RefreshComm(self):
		#self.controller.viewPage.dataWin.redraw()
		self.df = self.controller.viewPage.dataWin.pt.model.df
		self.df['Date Picked'] = self.df['Date Picked'].apply(lambda x: self.controller.getDatetime(x).date())

		self.df['Remind Date'] = self.df.apply(lambda row: (self.executeRefresh(row['Date Picked'], row['Maintenance Frequency'])), axis = 1)
		self.controller.viewPage.dataWin.pt.redraw()
		self.controller.saveDatabase()

		

	
	def executeRefresh(self, datePicked, maintFreq):
		datePickeddt = self.controller.getDatetime(datePicked)
		newDateRemind = datePickeddt + datetime.timedelta(days = int(maintFreq))
		newDateRemind = newDateRemind.date() 

		return newDateRemind
		

		#Reset Date remind
	def ExitComm(self):
		self.controller.parent.destroy()

		
###### CONTROLLER ######

class ControllerWin(ttk.Frame): 
	'''
	Main controller window called by main(). 
	Also contains multiple functions that affect other classes.
	Creates the notebook frame which the app is anchored in,
	grids three subclasses (arbitrarily named page 1-3).
	Pages are referenced in order of appearance. 
	Menubar created last, which gives options to save, refresh, or exit
	'''
	def __init__(self, parent):

		ttk.Frame.__init__(self, parent)
		self.parent = parent #parent is the root)
		start = timeit.default_timer()
		self.rootWidth = int(self.parent.winfo_screenwidth()*0.85)
		self.rootHeight = int(self.parent.winfo_screenheight()*0.85)
		self.rootFontSize = 11
		self.rootFont = 'Roboto'
		self.bgColor = 'white'
		self.fgColor = 'black'
		self.themeColor = 'white'##FCDFFC'
		self.parent.geometry('{}x{}'.format(self.rootWidth, self.rootHeight))
		self.parent.resizable(0,0)
		self.style = ThemedStyle(self.parent)
		#self.style.set_theme('breeze')
		#self.style = ttk.Style(parent)
		self.style.theme_use('vista') # *xpnative, winnative, *vista, classic, clam, alt
		self.style.configure('TFrame')
		self.style.configure('TLabelFrame')
		self.style.configure('TButton', font = (self.rootFont, self.rootFontSize))
		self.style.configure('TCheckbutton', font = (self.rootFont, self.rootFontSize))
		self.style.configure('TCombobox', font = (self.rootFont, self.rootFontSize))
		self.style.configure('TEntry', font = (self.rootFont, self.rootFontSize))
		self.style.configure('TLabel', font = (self.rootFont, self.rootFontSize))
		self.style.configure('Header.TLabelframe.Label', font = (self.rootFont, self.rootFontSize+1, 'bold'))
		self.style.configure('Bold.TLabel', font = (self.rootFont, self.rootFontSize+1, 'bold'))
		self.style.configure('TMenuButton', font = (self.rootFont, self.rootFontSize))
		self.style.configure('TNotebook', font = (self.rootFont, self.rootFontSize))
		self.style.configure('Horizontal.TScrollbar', font = (self.rootFont, self.rootFontSize))#, font=('Helvetica', 12))
		self.style.configure('Vertical.TScrollbar')#, font=('Helvetica', 12))#

		self.parent.grid_columnconfigure(0, weight=5)
		self.parent.grid_rowconfigure(0, weight=1)
		self.parent.grid_rowconfigure(1, weight = 1)




		self.notebook = ttk.Notebook(self.parent, height = int(self.rootHeight*0.7)) 
		self.notebook.grid(row = 0, column = 0, sticky='nesw', padx = 10, pady = 10)

		
		self.eventLogFrame = ttk.LabelFrame(self.parent, text = 'Event Log', style = 'Header.TLabelframe')
		self.eventLogFrame.grid(row = 1, column = 0, sticky='nesw', padx = 10, pady = 10)

		self.eventLog = tk.Text(self.eventLogFrame, height = 20) #Num lines
		self.eventLog.pack(expand = False, fill = 'x')

		stop = timeit.default_timer()


		start = timeit.default_timer()
		self.viewPage = viewpage.Create(self.notebook, self)
		stop = timeit.default_timer()
		print('ViewPage:',(stop-start))

		start = timeit.default_timer()
		self.entryPage = addpage.Create(self.notebook, self) #Self is the first reference of the omnipotent controller(win)
		stop = timeit.default_timer()
		print('EntryPage:',(stop-start))

		start = timeit.default_timer()
		self.toDoPage = todopage.Create(self.notebook, self)
		stop = timeit.default_timer()
		print('ToDoPage:',(stop-start))

		start = timeit.default_timer()
		self.expPage = planpage.Create(self.notebook, self)
		stop = timeit.default_timer()
		print('ExpPage:',(stop-start))

		start = timeit.default_timer()
		self.menubar = MenuBar(self.parent, self)
		self.entryMsg = ''
		self.writeEventLog(self.entryMsg)
		stop = timeit.default_timer()
		print('Else:',(stop-start))

	def writeEventLog(self, msg):
		
		numlines = int(self.eventLog.index('end - 1 line').split('.')[0])
		self.eventLog['state'] = 'normal'
		if numlines==20:
			self.eventLog.delete(1.0, 2.0)
		if self.eventLog.index('end-1c')!='1.0':
			self.eventLog.insert('end', '\n')
		self.eventLog.insert('end', msg)
		self.eventLog['state'] = 'disabled'

	def enterData(self):


		self.strainEntry = 	self.entryPage.strainvar.strain.get()

		if self.strainEntry == None or self.strainEntry == '':

			logMsg = '{}: No strain entered. Data will not be saved.'.format(datetime.datetime.now().replace(second=0, microsecond=0))
			self.writeEventLog(logMsg)
			return

		else:
			self.pickDateEntry = 	self.entryPage.pickDatevar.lastPick.get()
			self.constructEntry = 	self.entryPage.constructsvar.constructs.get()
			self.pickEveryEntry = 	self.entryPage.pickEvery.every.get()
			self.numPlatesEntry = 	self.entryPage.numPlatesvar.numPlates.get()
			self.locationEntry = 	self.entryPage.locationvar.location.get()
			self.notesEntry = 		self.entryPage.notesvar.notes.get()

			typeDict = self.entryPage.typevar.strainTypesDict
			typeEntry = ''
			for key in typeDict:
				boolean = typeDict.get(key).get() #1 = checked, 0 = unchecked
				if boolean == 1:
					if len(typeEntry) > 1: #already word in entry
						typeEntry = typeEntry + ', ' + key
						
					else: #Nothing in string yet
						typeEntry = str(key)
				typeDict.get(key).set(0)

			statusDict= self.entryPage.statusvar.statusDict
			statusEntry = ''
			for key in statusDict:
				boolean = statusDict.get(key).get() #1 = checked, 0 = unchecked
				if boolean == 1:
					if len(statusEntry) > 1: #already word in entry
						statusEntry = statusEntry + ', ' + key
					else: #Nothing in string yet
						statusEntry = str(key)
				else:
					continue
				statusDict.get(key).set(0)


			confirmMsg = 'Add {} to database?\n(Type: {}, Construct: {}, Status: {}'.format(
																							self.strainEntry, 
																							typeEntry, 
																							self.constructEntry, 
																							statusEntry
																							) #For pop up message
			#Create remind date from date picked and maint. freq. 

			try: 
				self.datepicked = datetime.datetime.strptime(self.pickDateEntry, '%m-%d-%Y')

			except ValueError:
				try: 
					self.datepicked = datetime.datetime.strptime(self.pickDateEntry, '%d-%m-%Y')
				except ValueError:
					try:
						self.datepicked = datetime.datetime.strptime(self.pickDateEntry, '%Y-%m-%d')
					except ValueError:
						pass 
			self.remindDateEntry = self.datepicked + datetime.timedelta(days = int(self.pickEveryEntry))
			self.remindDateEntry = self.remindDateEntry.date()


			dataRow = {'Name': self.strainEntry,
					 	'Date Picked': self.pickDateEntry,
						'Date Added': datetime.date.today(),
						'Strain Type': typeEntry,
						'Constructs': self.constructEntry,
						'Experimental Status': statusEntry,
						'Maintenance Frequency':self.pickEveryEntry,
						'Number of Plates': int(self.numPlatesEntry),
						'Location':self.locationEntry,
						'Notes': self.notesEntry,
						'Remind Date': self.remindDateEntry
					}

			self.addRowtoTable(dataRow)
			self.saveDatabase()

			logMsg = '{}: Saved {} to database'.format(datetime.datetime.now().replace(second=0, microsecond=0), self.strainEntry)

			self.writeEventLog(logMsg) #Write message to appear in log

			self.entryPage.strainvar.strain.delete(0, tk.END)
			self.entryPage.locationvar.location.delete(0, tk.END)
			self.entryPage.constructsvar.constructs.delete(0, tk.END)
			self.entryPage.pickEvery.every.set(self.entryPage.pickEvery.everyOptions[3])
			self.entryPage.numPlatesvar.numPlates.set(self.entryPage.numPlatesvar.numPlatesOptions[1])
			self.entryPage.notesvar.notes.delete(0, tk.END)

	def addRowtoTable(self, row):
		self.viewPage.dataWin.pt.model.df = self.viewPage.dataWin.pt.model.df.append(row, ignore_index = True)
		self.viewPage.dataWin.pt.redraw()

	def getData(self):
		self.data = pd.read_csv('app_files\\WormStrainsData.csv')
		#print('getData:', id(self.data), type(self.data))
		return self.data

	def getDatetime(self, date):
		date = str(date)

		if date == 'None':
			dtobject = 'None'

		try:
			dtobject = datetime.datetime.strptime(date, '%Y-%m-%d')

		except ValueError:
			try:
				dtobject = datetime.datetime.strptime(date, '%Y/%m/%d')
			except ValueError:
				try:
					dtobject = datetime.datetime.strptime(date, '%m-%d-%Y')
				except ValueError:
					try:
						dtobject = datetime.datetime.strptime(date, '%m/%d/%Y')
					except ValueError:
						try:
							dtobject = datetime.datetime.strptime(date, '%d-%m-%Y')
						except ValueError:
							try:
								dtobject = datetime.datetime.strptime(date, '%d/%m/%Y')
							except ValueError:
								return None
		return dtobject

	def getStrains(self):
		#Scrape strains that are 'pertinent' from local dataframe, located in the viewWin.
		#return shallow copy
		self.it = self.viewPage.dataWin.pt.model.df.copy(deep = False)
		#print('getStrains:', id(self.it), type(self.it))
		return self.it

	def saveDatabase(self):

		self.viewPage.dataWin.pt.model.df.to_csv('app_files\\WormStrainsData.csv', index = False)
		self.expPage.crossPage.currCrossTable.pt.model.df.to_csv('app_files\\exp_cross_data.csv', index = False)

##### END OF CLASSES #####

def initDB():
	
	if path.exists('app_files\\WormStrainsData.csv') == False:
		msg = 'Creating database'
		fields = ['Name', 'Date Picked', 'Date Added', 'Strain Type', 'Constructs', 'Experimental Status', 'Maintenance Frequency', 'Number of Plates', 'Location', 'Notes', 'Remind Date']
		blankrow = ['Example Strain', '2022-01-01', '2022-01-01', 'Array', 'olaEX3847', 'Crossing', '3', '2', 'Incubator 1, shelf 2', 'Delete this row', '2022-01-04']

		with open('app_files\\WormStrainsData.csv', 'w') as csvfile:
			csvwriter = csv.writer(csvfile)
			csvwriter.writerow(fields)
			csvwriter.writerow(blankrow)
			csvfile.close()

		return msg
	else:
		msg = 'Welcome!'
		return msg


def main():
	#start = timeit.default_timer()
	prepstrt = timeit.default_timer()
	initDB()
	root = tk.Tk()
	icon = tk.PhotoImage(file = 'app_files\\icon.png')
	root.iconphoto(True, icon)
	root.title('Worm Picker v4.0')
	root.grid_columnconfigure(0, weight = 1)
	ControllerWin(root)
	prepstop = timeit.default_timer()
	print('Main:', prepstop-prepstrt )
	stop = timeit.default_timer()
	print('Runtime:',(stop-gstart))
	root.mainloop()


main()