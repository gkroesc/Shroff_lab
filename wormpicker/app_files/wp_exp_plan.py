'''
Module for planning new experiments
'''

from os import path 
import tkinter as tk
from tkinter import ttk
import datetime
from pandastable import Table
#import csv
import pandas as pd 
import tkcalendar
#from ttkthemes import ThemedStyle

import wp_exp_data as export 

################################################
class Create(ttk.Frame):
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.parent = parent 
		self.controller = controller 

		self.mainframe = tk.Frame(self.parent)#, background = 'red') ####################################################################################################################################
		self.mainframe.grid(sticky='nesw')
		self.mainframe.grid_columnconfigure(0, weight=1)
		#self.mainframe.grid_columnconfigure(1, weight = 1)
		self.mainframe.grid_rowconfigure(0, weight=2)
		self.mainframe.grid_rowconfigure(1, weight = 1)	
		self.parent.add(self.mainframe, text='Experiments', sticky='nesw')

		self.expNotebook = ttk.Notebook(self.mainframe)
		self.expNotebook.grid(column = 0, padx = 5, pady = 5, sticky = 'nesw')

		self.crossPage = CrossExp(self.expNotebook, self.controller)

		self.weeklyCountandRefreshFrame = ttk.Frame(self.mainframe)
		self.weeklyCountandRefreshFrame.grid(row = 0, column = 1, pady = 5, padx = 5)

		self.weeklyCountFrame = ttk.LabelFrame(self.weeklyCountandRefreshFrame,
												 text = 'Weekly Plate Count', style = 'Header.TLabelframe')
		self.weeklyCountFrame.pack(side = 'bottom', fill = 'both', expand = False, pady = 5, padx = 5)
		self.weeklyCount = CrossCount(self.weeklyCountFrame, self.controller)
		self.refreshButton = ttk.Button(self.weeklyCountandRefreshFrame, text = 'Refresh',
										 command = lambda: (self.eventCalendar.refreshEvents(), self.crossPage.currCrossTable.refresh()))
		self.refreshButton.pack(side = 'top', fill = 'both', expand = False, pady = 5, padx = 5)

		self.eventCalendarFrame = ttk.Frame(self.mainframe)
		self.eventCalendarFrame.grid(row = 1, column = 0, pady = 5, sticky = 'nesw', columnspan = 2)
		self.eventCalendar = ExpCalendar(self.eventCalendarFrame, self.controller)



		##############################################

		
		#self.eventLogFrame = ttk.LabelFrame(self.mainframe, text = 'Event Log', style = 'Header.TLabelframe') ##############################################################################################
		#self.eventLogFrame.grid(column = 1, row = 0, padx=5, pady = 5,sticky = 'nesw', columnspan = 2, rowspan=2)

		#self.eventLog = tk.Text(self.eventLogFrame, height = 2, background = self.controller.themeColor)#) #Inside frame
		#self.eventLog.pack(anchor = 'n', fill = 'both', expand = True, padx = 5, pady = 5)
		#self.eventLog['state'] = 'disabled'

class CrossExp(ttk.Frame):
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.parent = parent 
		self.controller = controller 
		self.title = 'Cross'
		self.errMsg = "Use 'Strains' dropdown menus to select strains to cross."
		self.errMsgPlate = "Use 'Date' and '# of Plates' drop down menus to specify experiment details"

		self.data = {}

		self.mainframe = ttk.Frame(self.parent)
		self.parent.add(self.mainframe, text='Cross', sticky='nesw')

		self.planBox = ttk.LabelFrame(self.mainframe, text = 'Plan: {}'.format(self.title), 
										height = self.controller.rootHeight -100, 
										width = self.controller.rootWidth/2, 
										style = 'Header.TLabelframe')

		self.planBox.pack(expand = True, fill = 'both', side = 'left', pady = 5, padx = 5)#.grid(column = 0, sticky = 'nesw', pady=(10,0), padx = 5)

		self.currCrossBox = ttk.LabelFrame(self.mainframe, text = 'Current Crosses',
										style = 'Header.TLabelframe')
		self.currCrossBox.pack(expand = True, fill = 'both', side = 'left', pady = 5, padx = 5)#grid(column = 1, row = 0, sticky = 'nesw', pady=5, padx = 5 )

		self.currCrossTable = CurrCrosses(self.currCrossBox, self.controller)

		


		
		self.strainSelectLabel = ttk.Label(self.planBox, text = 'Strains')
		self.strainSelectLabel.grid(row = 0, column = 0, sticky = 'w')

		self.strainSelectFrame = ttk.Frame(self.planBox)
		self.strainSelectFrame.grid(row = 0, column = 1, pady = 5, padx = 5, sticky = 'w')
		self.strain1 = StrainSelect(self.strainSelectFrame, self.controller)
		self.strain1.strainSelectFrame.grid(row = 0, column = 1)
		self.crossSymbol = ttk.Label(self.strainSelectFrame, text = ' X ', style = 'Bold.TLabel').grid(row = 0, column = 2)
		self.strain2 = StrainSelect(self.strainSelectFrame, self.controller)
		self.strain2.strainSelectFrame.grid(row = 0, column = 3)
		self.data['Strain1'] = self.strain1.strain
		self.data['Strain2'] = self.strain2.strain



		self.p0Label = ttk.Label(self.planBox, text = 'P0 Date')
		self.p0Label.grid(row = 1, column = 0, sticky = 'w')
		self.p0Frame = ttk.Frame(self.planBox)
		self.p0Frame.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'w')
		self.p0date = DateSelect(self.p0Frame, self.controller)
		self.p0date.dateFrame.grid(row = 0, column = 1)	
		self.p0numPlates = NumPlatesSelect(self.p0Frame, self.controller)
		self.p0numPlates.plateSelectFrame.grid(row = 0, column = 2)
		self.data['p0_date'] = self.p0date.datevar
		self.data['p0_num_plates'] = self.p0numPlates.numPlates


		self.f1Label = ttk.Label(self.planBox, text = 'F1 Date')
		self.f1Label.grid(row = 2, column = 0, sticky = 'w')
		self.f1Frame = ttk.Frame(self.planBox)
		self.f1Frame.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = 'w')
		self.f1date = DateSelect(self.f1Frame, self.controller)
		self.f1date.dateFrame.grid(row = 0, column = 1)
		self.f1numPlates = NumPlatesSelect(self.f1Frame, self.controller)
		self.f1numPlates.plateSelectFrame.grid(row = 0, column = 2)
		self.data['f1_date'] = self.f1date.datevar
		self.data['f1_num_plates'] = self.f1numPlates.numPlates


		self.f2Label = ttk.Label(self.planBox, text = 'F2 Date')
		self.f2Label.grid(row = 3, column = 0, sticky = 'w')
		self.f2Frame = ttk.Frame(self.planBox)
		self.f2Frame.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = 'w')
		self.f2date = DateSelect(self.f2Frame, self.controller)
		self.f2date.dateFrame.grid(row = 0, column = 1)
		self.f2numPlates = NumPlatesSelect(self.f2Frame, self.controller)
		self.f2numPlates.plateSelectFrame.grid(row = 0, column = 2)
		self.data['f2_date'] = self.f2date.datevar
		self.data['f2_num_plates'] = self.f2numPlates.numPlates

		self.f3Label = ttk.Label(self.planBox, text = 'F3 Date')
		self.f3Label.grid(row = 4, column = 0, sticky = 'w')
		self.f3Frame = ttk.Frame(self.planBox)
		self.f3Frame.grid(row = 4, column = 1, padx = 5, pady = 5, sticky = 'w')
		self.f3date = DateSelect(self.f3Frame, self.controller)
		self.f3date.dateFrame.grid(row = 0, column = 1)
		self.f3numPlates = NumPlatesSelect(self.f3Frame, self.controller)
		self.f3numPlates.plateSelectFrame.grid(row = 0, column = 2)
		self.data['f3_date'] = self.f3date.datevar
		self.data['f3_num_plates'] = self.f3numPlates.numPlates

		self.colorNotesLabel = ttk.Label(self.planBox, text = 'Fluorescence Notes')
		self.colorNotesLabel.grid(row = 5, column = 0, sticky = 'w')
		self.colorNotesEntry = ttk.Entry(self.planBox)
		self.colorNotesEntry.grid(row = 5, column = 1, sticky = 'w', padx = 5, pady = 5)
		self.data['color_notes'] = self.colorNotesEntry

		self.expNotesLabel = ttk.Label(self.planBox, text = 'Experiment Notes')
		self.expNotesLabel.grid(row = 6, column = 0, sticky = 'w')
		self.expNotesEntry = ttk.Entry(self.planBox)
		self.expNotesEntry.grid(row = 6, column = 1, sticky = 'w', padx=5, pady=5)
		self.data['experiment_notes'] = self.expNotesEntry

		self.submitButton = ttk.Button(self.planBox, text = 'Submit', command = lambda: self.submit())
		self.submitButton.grid(row = 7, column = 0, columnspan = 2, sticky = 'ew', padx = 5, pady = 5)


	def submit(self):
		'''
		function that submits all cross data to exp_data.py
		'''
		
		

		self.getData = {}
		for self.key in self.data.keys():
			self.getData[self.key] = self.data[self.key].get()
		
		if self.getData['Strain1'] == 'Strain Name [Construct]' or self.getData['Strain1'] == 'None':
			self.controller.writeEventLog(self.errMsg)
			return
		elif self.getData['Strain2'] == 'Strain Name [Construct]' or self.getData['Strain2'] == 'None':
			self.controller.writeEventLog(self.errMsg)
			return
		elif self.getData['p0_date'] == 'None' or self.getData['p0_date'] == None:
			self.controller.writeEventLog(self.errMsgPlate)
			return

		export.writeCross(self.getData)

		for self.key in self.data.keys():
			try: 
				self.data[self.key].delete(0, tk.END)
			except AttributeError:
				try:
					self.data[self.key].set('None')
				except AttributeError:
					pass 

		msg = "Cross Scheduled for {} x {}:\n\t\t P0: {}\n\t\t F1: {}\n\t\t F2: {}\n\t\t F3: {}".format(
																									self.getData['Strain1'], 
																									self.getData['Strain2'],
																									self.getData['p0_date'],
																						 			self.getData['f1_date'], 
																						 			self.getData['f2_date'],
																						 			self.getData['f3_date'])
		self.controller.writeEventLog(msg)



class ExpCalendar(ttk.Frame):
	def __init__(self, parent, controller):#, row, column):
		ttk.Frame.__init__(self, parent)
		self.parent = parent
		self.controller = controller 
		#self.keyFrame = ttk.Frame()
		self.calFrame = ttk.Frame(self.parent)
		self.calFrame.pack(side = 'left', fill = 'both', expand = True, padx = 5, pady = 5)

		self.expCal = tkcalendar.Calendar(
											self.calFrame, 
											background = 'black',
											showothermonthdays = False,
											selectmode = 'day', 
											tooltipdelay = 2,
											tooltipbackground = '#ffe0f9',
											tooltipforeground = 'black',
											selectbackground = '#939995')
		self.expCal.pack(side = 'left', anchor = 'n',fill = 'both', expand = True, padx = 5, pady = 5)
		

		self.captionFrame = ttk.LabelFrame(self.parent, text = 'Description', style = 'Header.TLabelframe')
		self.captionFrame.pack(side= 'right', fill = 'both', expand = True, padx = 5, pady = 5)
		self.caption = tk.Text(self.captionFrame, height = 10)#) #Inside frame
		self.caption.pack(fill = 'both', expand = False)
		self.caption['state'] = 'disabled'

		self.fillEvents()

		self.expCal.bind('<<CalendarSelected>>', lambda x: self.displayEvents())

		#self.expCal.tag_config('P0', background = '#f78181')
		#self.expCal.tag_config('F1', background = '#f7d881')
		#self.expCal.tag_config('F2', background = '#61cf7b')
		#self.expCal.tag_config('F3', background = '#52adf7')
		self.expCal.tag_config('cross', background = '#f7d881', foreground = 'black')

		self.expCal.selection_set(datetime.date.today())
		self.expCal.selection_clear()

	def refreshEvents(self):
		self.expCal.calevent_remove('all')
		self.fillEvents()
		self.controller.expPage.crossPage.currCrossTable.fillTable()


	def displayEvents(self):
		self.caption['state'] = 'normal'
		self.caption.delete(1.0, 'end')



		date = self.expCal.selection_get()
		self.myid = self.expCal.get_calevents(date)
		for i in self.myid:
			event = self.expCal.calevent_cget(ev_id = i, option = 'text')
			print(event)
			msg = '{}: {}'.format(date, event)
			print(msg)
			self.caption.insert('end', msg)
			self.expCal.selection_set(date)


		self.caption['state'] = 'disabled'
		self.expCal.selection_set(date)


	def fillEvents(self):
		if path.exists('app_files\\exp_cross_data.csv') == False:
			pass
		else:
			self.evdf = pd.read_csv('app_files\\exp_cross_data.csv')
			self.evcols = list(self.evdf.columns)
			self.evls = self.evdf.values.tolist()

			ls = ['P0', 'F1', 'F2', 'F3']
			for row in self.evls:
				for i in range(0,4):
					s1 		= row[0]
					s2 		= row[1]
					date 	= row[2+(2*i)]
					p 		= row[3+(2*i)]
					#text 	= '{} x {} || {}: {} plates'.format(s1, s2, ls[i], p)
					text = '{}: {} x {} to {} plates'.format(ls[i], s1, s2, p)
					date = self.controller.getDatetime(date)
					
					
					try:
						self.expCal.calevent_create(date = date, text = text, tags = 'cross')
						self.expCal.selection_set(date)
					except TypeError:
						#TypeError likely arises from unspecified experiment date. Ex: 'None' for F3_date
						break

class CurrCrosses(ttk.Frame):

	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.controller = controller
		self.parent = parent
		self.viewWindow = ttk.Frame(self.parent)
		self.viewWindow.pack(fill = 'both', expand=True)
		self.fillTable()

	def fillTable(self):
		self.df = export.readCross()
		self.table = self.pt = Table(self.viewWindow, dataframe = self.df)
		self.pt.show()


	def refresh(self):
		self.pt.redraw()
	'''
	For now, just create labels that display the crosses, but may need to complicate it later,


	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.parent = parent
		self.controller = controller

		if path.exists('exp_cross_data.csv'):
			self.evdf = pd.read_csv('exp_cross_data.csv')
			evls = self.evdf.values.tolist()
			for i in range(len(evls)):
				for j in reversed(range(3,10,2)): #Starts at latest date (F3), if date has passed, pass. If upcoming, grid it)
					date = evls[i][j]
					if date == '' or date == 'None':
						continue

					elif self.controller.getDatetime(date) > datetime.datetime.today():
						ttk.Label(self.parent, text = '<<{}>> x <<{}>>'.format(evls[i][1], evls[i][2])).grid(column = 0,
																										row = i,
																										padx = 5,
																										pady = 5,
																										sticky = 'nesw')
						ttk.Button(self.parent, text = 'Edit').grid()

						break
					elif self.controller.getDatetime(date) < datetime.datetime.today():

						break
					else:
						continue						
	'''

class CrossCount(ttk.Frame):
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.parent = parent
		self.controller = controller

		self.weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

		self.weekdaycount = {}

		todaywd = datetime.datetime.today().weekday()
		for i in range(todaywd,todaywd+7): #Creates respective list starting at today, ending 6 days from now
			if (i+1) >7:				   #Puts days in order starting with today
				self.weekdaycount[i-7] = 0
			else:
				self.weekdaycount[i] = 0

		if path.exists('app_files\\exp_cross_data.csv') == True:
			self.weekdaycount = self.getDayCounts()

		myrow = 0
		total = 0
		for key in self.weekdaycount:

			ttk.Label(self.parent, text = self.weekdays[key]+':').grid(column = 0, row = myrow, sticky = 'e')
		
			#Count label
			ttk.Label(self.parent, text = self.weekdaycount[key]).grid(column = 1, row = myrow, sticky = 'w')
			total += self.weekdaycount[key]
			myrow += 1

		ttk.Label(self.parent, text = 'Total:').grid(column = 0, row = myrow, sticky = 'e')
		
		#Count label
		ttk.Label(self.parent, text = total).grid(column = 1, row = myrow, sticky = 'w')


	
	def getDayCounts(self):

		self.maxDay = (datetime.datetime.today() + datetime.timedelta(weeks=1)).replace(hour = 0, minute = 0, second = 0, microsecond = 0)
		self.minDay = datetime.datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
		ls = ['P0', 'F1', 'F2', 'F3']
		self.evdf = pd.read_csv('app_files\\exp_cross_data.csv')
		self.evcols = list(self.evdf.columns)
		self.evls = self.evdf.values.tolist()
		for row in self.evls:
			for i in range(0,4):
				date 	= row[2+(2*i)]
				p 		= row[3+(2*i)]

				dt = self.controller.getDatetime(date)

				try:
					
					if dt > self.maxDay:
						pass 
					elif dt < self.minDay:
						pass 
					else:
						self.weekdaycount[dt.weekday()] += int(p)
				except TypeError:
					#date == None or 'None'
					pass 
				except ValueError:
					# #plates == None or 'None'
					pass
		return self.weekdaycount


			#Get the date of each day, find corresponding Exp Stage, # of plates. 

class StrainSelect(ttk.Frame):
	'''
	Create dropdown menu that allows user to select a strain from the database
	'''
	def __init__(self, parent, controller):

		ttk.Frame.__init__(self, parent)
		self.controller = controller
		self.parent = parent
		self.strainSelectFrame = tk.Frame(self.parent, bg = 'black')

		self.strain = tk.StringVar(self.strainSelectFrame)
		self.strain.set('None')
		self.strainOptions = self.strainList()
		self.strainMenu = ttk.OptionMenu(self.strainSelectFrame, self.strain, *self.strainOptions)

		self.strainMenu.pack(fill = 'both', expand = True, padx = 1, pady = 1)

	def strainList(self):
		self.ls = ['Strain Name [Construct]']
		self.df = self.controller.getStrains()
		self.df = self.df.fillna('None')
		self.names = self.df['Name'].tolist()
		self.constructs = self.df['Constructs'].tolist()
		self.strtype = self.df['Strain Type'].tolist()

		for i in range(len(self.names)):
			if 'Males' in self.strtype[i]:
				self.ls.append('{} [{}] [Male]'.format(self.names[i], self.constructs[i]))
			else:
				self.ls.append('{} [{}]'.format(self.names[i], self.constructs[i]))

		return self.ls

class DateSelect(ttk.Frame):
	'''
	Create date menu
	'''
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.parent = parent
		self.controller = controller 

		self.datevar = tk.StringVar()

		self.dateFrame = ttk.Frame(self.parent)
		self.date = tkcalendar.DateEntry(self.dateFrame ,selectmode='day', textvariable = self.datevar, date_pattern = 'yyyy-MM-dd')
		self.datevar.set('None')
		self.date.pack(fill = 'both', expand = True)

class NumPlatesSelect(ttk.Frame):
	def __init__(self, parent, controller):
		self.parent = parent
		self.controller = controller 

		self.plateSelectFrame = ttk.Frame(self.parent)

		self.numPlates = tk.StringVar(self.plateSelectFrame)
		self.numPlatesOptions = []
		for i in range(0,21):
			self.numPlatesOptions.append(int(i))
		self.numPlates.set('None')

		ttk.Label(self.plateSelectFrame, text = '# of Plates: ').grid(row = 0, column = 0, sticky = 'w', padx = 5)
		
		self.numPlatesMenu = ttk.OptionMenu(self.plateSelectFrame, self.numPlates, *self.numPlatesOptions)
		self.numPlatesMenu.grid(row=0, column=1,sticky='w')

		ttk.Label(self.plateSelectFrame, text = 'plate(s)').grid(row=0, column = 2, sticky='w')

