"""
Worm picker v.2

01/24/22
Utilize modified model-view-controller framework

view-controller

use classes

Icon Created with BioRender.com
"""
from os import path 
import tkinter as tk
from tkinter import ttk
import datetime
from pandastable import Table
import csv
import pandas as pd 
from tkcalendar import DateEntry


####### CLASSES #######

### PAGE 1: Entry ###

class page1(ttk.Frame):
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.parent = parent
		self.controller = controller 

		self.addWin = tk.Frame(self.parent) #Width has no effect
		self.addWin.grid(sticky='nesw')
		self.parent.add(self.addWin, text='Add new strain', sticky='nesw')
		#self.addWin.grid_columnconfigure(0, weight=1)


		self.addBox = tk.LabelFrame(self.addWin, text='Strain Variables')
		self.addBox.grid(column=0, sticky = 'nw', padx=20, pady=0)
		self.addBox.grid_columnconfigure(0, weight=1)
		self.addBox.grid_rowconfigure(7, weight  = 1)

		self.eventLogFrame = tk.LabelFrame(self.addWin, text = 'Event Log')#, background='cyan')
		self.eventLogFrame.grid(column = 1, row = 0, sticky = 'nw')
		self.eventLogFrame.grid_columnconfigure(1, weight=1)

		self.eventLog = tk.Text(self.eventLogFrame)#) #Inside frame
		self.eventLog.grid(sticky = 'nesw')
		self.eventLog.grid_columnconfigure(0, weight=1)


		### Variables
		self.strainvar = strainClass(self.addBox, self.controller) #self.controller is a downstream reference to ControllerWin
		self.typevar = typeClass(self.addBox, self.controller) 
		self.constructsvar = constructsClass(self.addBox, self.controller) 
		self.statusvar = statusClass(self.addBox, self.controller) 
		self.pickDatevar = PickDateClass(self.addBox, self.controller)
		self.notesvar = notesClass(self.addBox, self.controller)
		self.pickEvery =  PickEveryClass(self.addBox, self.controller)

		### Getting
		self.enterButton = tk.Button(self.addBox, text = 'Enter', width=25, command = (lambda:self.controller.enterData())) 

		self.enterButton.grid(columnspan = 2, row=7, column=0, pady=5, padx=5) 
class strainClass(ttk.Frame):#var=self.strain
	def __init__(self, addBox, controller):

		ttk.Frame.__init__(self, addBox)
		self.controller = controller
		self.addBox = addBox 

		tk.Label(self.addBox, text='Strain Name').grid(row = 0, sticky='w', pady=5)
		self.strain = tk.Entry(self.addBox)
		self.strain.grid(row=0, column=1, sticky='w', padx=5)
class typeClass(ttk.Frame):#var=self.strainTypeVar
	def __init__(self, addBox, controller):

		ttk.Frame.__init__(self, addBox)
		self.controller = controller
		self.addBox = addBox

		
		
		self.No = tk.IntVar()
		self.In = tk.IntVar()
		self.Ar = tk.IntVar()
		self.Hs = tk.IntVar()
		self.Ma = tk.IntVar()

		self.strainTypesDict = {'None': self.No, 'Integrated': self.In, 'Array':self.Ar, 'Heat shock':self.Hs, 'Males':self.Ma}

		tk.Label(self.addBox, text= 'Type').grid(row = 1, sticky= 'nw', pady=5)
		self.checkFrame = tk.Frame(self.addBox)
		self.checkFrame.grid(row=1, column = 1, sticky='w')

		self.NoCheck = tk.Checkbutton(self.checkFrame, text = 'None', variable = self.No ).grid(row = 0, sticky='w')
		self.InCheck = tk.Checkbutton(self.checkFrame, text = 'Integrated', variable = self.In ).grid(row = 1, sticky='w')
		self.ArCheck = tk.Checkbutton(self.checkFrame, text = 'Array', variable = self.Ar).grid(row = 2, sticky='w')
		self.HsCheck = tk.Checkbutton(self.checkFrame, text = 'Heat Shock', variable = self.Hs).grid(row =3, sticky='w')
		self.MaCheck = tk.Checkbutton(self.checkFrame, text = 'Males', variable = self.Ma).grid(row = 4, sticky='w')

		#self.strainTypeVar = tk.StringVar(self.addBox)
		#self.strainTypeVar.set(self.strainTypesls[0]) # default value
		#self.typeMenu = tk.OptionMenu(self.addBox, self.strainTypeVar, *self.strainTypesls)
		#self.typeMenu.grid(row=1, column=1, sticky='w', padx=5)
class constructsClass(ttk.Frame):#var=self.constructs
	def __init__(self, addBox, controller):

		ttk.Frame.__init__(self, addBox)
		self.controller = controller
		self.addBox = addBox

		tk.Label(self.addBox, text= 'Construct').grid(row= 2, sticky= 'w', pady=5)
		self.constructs = tk.Entry(self.addBox) 
		self.constructs.grid(row=2, column=1, sticky='w', padx=5)
class statusClass(ttk.Frame):#var=self.status
	def __init__(self, addBox, controller): 
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

		tk.Label(self.addBox, text= 'Experimental Status').grid(row=3, sticky='nw', pady=5)
		self.checkFrame = tk.Frame(self.addBox)

		self.checkFrame.grid(row = 3, column = 1, sticky = 'w')
		self.NoCheck = tk.Checkbutton(self.checkFrame, text = 'None', variable = self.No ).grid(row = 0, sticky='w')
		self.MaCheck = tk.Checkbutton(self.checkFrame, text = 'Maintaining', variable = self.Ma ).grid(row = 1, sticky='w')
		self.ImCheck = tk.Checkbutton(self.checkFrame, text = 'Imaged', variable = self.Im ).grid(row = 2, sticky='w')
		self.StCheck = tk.Checkbutton(self.checkFrame, text = 'Crossing', variable = self.St ).grid(row = 3, sticky='w')
		self.ScCheck = tk.Checkbutton(self.checkFrame, text = 'Screening', variable = self.Sc ).grid(row = 4, sticky='w')
		self.LiCheck = tk.Checkbutton(self.checkFrame, text = 'Lineaging', variable = self.Li ).grid(row = 5, sticky='w')
		self.CtCheck = tk.Checkbutton(self.checkFrame, text = 'Currently tracking', variable = self.Ct ).grid(row = 6, sticky='w')

		
		#self.status = tk.StringVar(self.addBox)
		#self.status.set(self.statusls[0]) # default value
		#self.statusMenu = tk.OptionMenu(self.addBox, self.status, *self.statusls)
		#self.statusMenu.grid(row=3, column=1, sticky='w', padx=5)

class PickDateClass(ttk.Frame):
	def __init__(self, addBox, controller):
		ttk.Frame.__init__(self, addBox)
		self.addBox = addBox
		self.controller = controller 

		self.lastPick = tk.StringVar()

		self.pickLabel = tk.Label(self.addBox, text = 'Last Day Picked:')
		self.pickLabel.grid(row = 4 , column =0 , sticky = 'w')

		self.date = DateEntry(self.addBox,selectmode='day', textvariable = self.lastPick, date_pattern = 'yyyy-MM-dd')
		self.date.grid(row=4,column=1,pady=5, sticky = 'w')

class PickEveryClass(ttk.Frame):
	def __init__(self, addBox, controller):
		self.addBox = addBox
		self.controller = controller 
		self.every = tk.StringVar(self.addBox)
		self.everyOptions = []
		for i in range(1,15):
			self.everyOptions.append(int(i))
		self.every.set(self.everyOptions[3])

		tk.Label(self.addBox, text = 'Maintain every').grid(row = 5, column = 0, sticky = 'w')
		
		self.pickEveryMiniFrame = tk.Frame(self.addBox)
		self.pickEveryMiniFrame.grid(row = 5, column = 1, sticky='w', pady=5)

		self.everyMenu = tk.OptionMenu(self.pickEveryMiniFrame, self.every, *self.everyOptions).grid(row=0, column=0,sticky='w')
		tk.Label(self.pickEveryMiniFrame, text = 'day(s)').grid(row=0, column = 1, sticky='w')

class notesClass(ttk.Frame): #var=self.notes
	def __init__(self, addBox, controller): #addBox == parent
		ttk.Frame.__init__(self, addBox)
		self.controller = controller
		self.addBox = addBox
		tk.Label(self.addBox, text = 'Notes').grid(row=6, sticky='w', pady=5)
		self.notes = tk.Entry(self.addBox)
		self.notes.grid(row=6, column=1, sticky='w', padx=5)
### PAGE 2: View Database ###
class page2(ttk.Frame):
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)

		self.parent = parent 
		self.controller = controller
		self.page2Frame = tk.Frame(self.parent)
		self.page2Frame.grid()
		self.page2Frame.grid_columnconfigure(0, weight=1)
		self.parent.add(self.page2Frame, text = 'View database strains') #Add tab to NB

		self.dataWin = dataView(self.page2Frame, self.controller)
 
class dataView(ttk.Frame):
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.controller = controller
		self.parent = parent
		self.viewWindow = tk.Frame(self.parent)
		#self.viewWindow.grid(sticky='nesw')
		#self.viewWindow.grid_columnconfigure(0, weight=1)
		self.viewWindow.pack(fill = 'both', expand=True)
		self.df = self.controller.getData() 
		#print('dataview:', id(self.df), type(self.df))

		self.table = self.pt = Table(self.viewWindow, dataframe = self.df)
		self.pt.show()

	#def addRowtoTable(self, row):
	#	self.pt.model.df = self.pt.model.df.append(row, ignore_index = True)
	#	print('addRow:', id(self.pt.model.df), type(self.pt.model.df))
	#	self.pt.redraw()


	def refresh(self): #To fully refresh, the csv would need to be saved, closed, then opened again and
						# loaded into the table via self.pt.model.df = pd.read_csv('WormStrainsData.csv')
						# Then redrawn again. Shouldn't really be necessary unless multiple users at same time. 
		self.pt.redraw()

	#def savetocsv(self):
	#	self.pt.model.df.to_csv('WormStrainsData.csv', index = False)
	#	self.df = self.controller.getData()
	#	self.table = self.pt = Table(self.viewWindow, dataframe = self.df)
	#	print('savetocsv:', id(self.df), type(self.df))
	#	self.pt.redraw()
	
### PAGE 3: To-Do ###

class page3(ttk.Frame):
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.parent = parent 
		self.controller = controller

		self.toDoWin = tk.Frame(self.parent) #Width has no effect
		self.toDoWin.grid(sticky='nesw')
		self.toDoWin.grid_columnconfigure(0, weight=1)
		self.toDoWin.grid_rowconfigure(0, weight=1)
		self.parent.add(self.toDoWin, text='To-Do List', sticky='nesw')


		self.pickBox = tk.Frame(self.toDoWin)
		self.pickBox.pack(fill = 'both', expand = True)
		self.pickBox.grid_rowconfigure(0, weight=1)
		self.pickBox.grid_columnconfigure(0, weight=1)

		self.childPickFrame = strainsToPick(self.pickBox, self.controller)

	def writeTaskEventLog(self, msg):
		
		numlines = int(self.childPickFrame.eventLog.index('end - 1 line').split('.')[0])
		self.childPickFrame.eventLog['state'] = 'normal'
		if numlines==24:
			self.childPickFrame.eventLog.delete(1.0, 2.0)
		if self.childPickFrame.eventLog.index('end-1c')!='1.0':
			self.childPickFrame.eventLog.insert('end', '\n')
		self.childPickFrame.eventLog.insert('end', msg)
		self.childPickFrame.eventLog['state'] = 'disabled'


class strainsToPick(ttk.Frame):
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.parent = parent
		self.controller = controller

		self.refineddf = self.refine()
		self.names = self.refineddf['Name'].tolist()
		self.namesVar = tk.StringVar(value = self.names)

		self.pickListFrame = tk.Frame(self.parent)
		self.pickListFrame.grid(column = 0, sticky = 'nesw')
		self.pickListFrame.grid_columnconfigure(2, minsize = 250)
		self.pickListFrame.grid_columnconfigure(4, weight = 1)
		self.pickListFrame.grid_rowconfigure(0, weight = 1)

		self.pickListBox = tk.Listbox(self.pickListFrame, height = 10, width = 30, listvariable = self.namesVar, selectmode = 'browse')
		self.pickListBox.grid(column = 0, row = 0, sticky = 'nsw', padx=(25,0), pady = (10,0))
		self.pickListBox.bind('<<ListboxSelect>>', lambda a: self.descriptions())

		self.vscroll = ttk.Scrollbar(self.pickListFrame, orient= 'vertical', command = self.pickListBox.yview)
		self.vscroll.grid(column = 1, row = 0, sticky = 'nws', padx=(0,15))
		self.pickListBox['yscrollcommand'] = self.vscroll.set
 
		self.descboxborder = tk.Frame(self.pickListFrame)
		self.descboxborder.grid(column = 2, row = 0, sticky = 'nesw', pady=(5,0))

		#self.descboxborder.grid_columnconfigure(0, weight = 1)
		self.descbox = tk.LabelFrame(self.descboxborder, text = 'Description')
		self.descbox.pack(fill = 'both', expand = True)
		#self.descbox.pack(fill = 'both', expand = True, padx = 1, pady = 1)
		#self.descbox.grid_columnconfigure(1, weight = 1)

		self.eventLogFrame = tk.LabelFrame(self.pickListFrame, text = 'Event Log')#, background='cyan')
		self.eventLogFrame.grid(column = 4, row = 0, sticky = 'nse', padx = 5, pady = 5)
		

		self.eventLog = tk.Text(self.eventLogFrame)#) #Inside frame
		self.eventLog.grid(padx=5,sticky = 'nesw')

		self.dsmsg = tk.StringVar()
		self.dpmsg = tk.StringVar() #date picked
		self.stmsg = tk.StringVar() #strain type
		self.comsg = tk.StringVar() #constructs
		self.exmsg = tk.StringVar() #experimental status
		self.nomsg = tk.StringVar() #notes

		self.dstitle = tk.Label(self.descbox, text = 'Days Since Last Pick:')
		self.dptitle = tk.Label(self.descbox, text = 'Last Date Picked:' )
		self.sttitle = tk.Label(self.descbox, text = 'Strain Type:')
		self.cotitle = tk.Label(self.descbox, text = 'Constructs:')
		self.extitle = tk.Label(self.descbox, text = 'Experimental Status:')
		self.notitle = tk.Label(self.descbox, text = 'Notes:')

		self.dsdesc = tk.Label(self.descbox, textvariable = self.dsmsg)
		self.dpdesc = tk.Label(self.descbox, textvariable = self.dpmsg)
		self.stdesc = tk.Label(self.descbox, textvariable = self.stmsg)
		self.codesc = tk.Label(self.descbox, textvariable = self.comsg)
		self.exdesc = tk.Label(self.descbox, textvariable = self.exmsg)
		self.nodesc = tk.Label(self.descbox, textvariable = self.nomsg)

		self.titles = [self.dstitle, self.dptitle, self.sttitle, self.cotitle,
						self.extitle, self.notitle]
		self.descs = [self.dsdesc, self.dpdesc, self.stdesc, self.codesc,
						self.exdesc, self.nodesc]

		for i in range(len(self.titles)):
			self.titles[i].grid(row = i, column = 0, sticky = 'e')
			self.descs[i].grid(row = i, column = 1, sticky = 'w')


		self.dsmsg.set('')
		self.dpmsg.set('')
		self.stmsg.set('')
		self.comsg.set('')
		self.exmsg.set('')
		self.nomsg.set('')

		self.snoozeorpick = SnoozePickButtons(self.descbox, self.controller)

	def descriptions(self):

		self.idxs = self.controller.toDoPage.childPickFrame.pickListBox.curselection()
		if len(self.idxs) == 1:

			self.idx = int(self.idxs[0])
			
			self.dsmsg.set(self.refineddf['Days Since'].values[self.idx])
			self.dpmsg.set(self.refineddf['Date Picked'].values[self.idx])
			self.stmsg.set(self.refineddf['Strain Type'].values[self.idx])
			self.comsg.set(self.refineddf['Constructs'].values[self.idx])
			self.exmsg.set(self.refineddf['Experimental Status'].values[self.idx])
			self.nomsg.set(self.refineddf['Notes'].values[self.idx])

		self.controller.toDoPage.childPickFrame.snoozeorpick.snoozeVar.set('Snooze')

	def refine(self):

		"""refine df"""
		self.df2 = self.controller.getStrains() #temporary dataframe
		self.df2.dropna(subset = ['Date Picked'], axis = 0, inplace = True) #If no date picked, then drop it in temp file
		self.df2['Today'] = datetime.datetime.today()
		self.df2['Days Since'] = self.df2.apply(lambda row: (self.calcDaysSince(row['Today'], row['Date Picked'])).days, axis=1)

		self.df2['Ready'] = self.df2.apply(lambda row: (self.calcDaysUntil(row['Today'], row['Remind Date'])), axis = 1)

		pd.to_timedelta(self.df2['Maintenance Frequency'], unit = 'days')

		#self.df2 = self.df2[self.df2['Days Since'] >= self.df2['Maintenance Frequency']]	#Strains where days since is greater than

		self.df2 = self.df2[self.df2['Ready'] == True]

		""" Splitting DFs between old and current. """
		self.df2Old = self.df2[self.df2['Days Since'] > 30]

		self.df2 = self.df2[self.df2['Days Since'] <=30]

		"""Sorting Current and adding old to it after"""
		self.df2.sort_values(['Days Since'], ascending = False, inplace = True)
		self.df2 = self.df2.append(self.df2Old)
		self.df2.drop(labels= ['Date Added', 'Maintenance Frequency', 'Today'], axis = 1, inplace = True)
		self.df2.fillna('None', inplace = True)

		return self.df2

	def getDatetime(self, date):
		date = str(date)
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

	def calcDaysSince(self, todayDate, datePicked):
		datePicked = str(datePicked)
		daysSince = todayDate - self.getDatetime(datePicked)
		return daysSince

	def calcDaysUntil(self, todayDate, remindDate):
		#Return boolean if remind date is today?
		remindDate = str(remindDate)
		daysUntil = self.getDatetime(remindDate) - todayDate

		if daysUntil.days <= 0: #If daysuntil has passed or is 0
			return True
		else:
			return False

class SnoozePickButtons(ttk.Frame):
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.parent = parent
		self.controller = controller 
		self.pt = self.controller.viewPage.dataWin.pt
		#print('SnoozePickButtons:', id(self.pt.model.df), type(self.pt.model.df))

		self.buttonFrame = tk.Frame(self.parent)
		self.buttonFrame.grid(row = 10, column = 0, columnspan=2, sticky = 'w')

		self.pickedButton = tk.Button(self.buttonFrame, text = 'Mark as Picked', width = 13, command = lambda: self.pickedRemind())

		self.snoozeList = ['1 Day', '2 Days', '3 Days', '4 Days']
		self.snoozeVar = tk.StringVar()

		self.snoozeVar.set('Snooze')
		self.snoozeMenu = tk.OptionMenu(self.buttonFrame, self.snoozeVar, *self.snoozeList, command = lambda x: self.showSnoozeButton())
		self.deleteButton = tk.Button(self.buttonFrame, text = 'Delete Strain', width = 13, command = lambda: self.deleteRemind())

		self.pickedButton.grid(row=0, pady=5,padx=(10,15), sticky = 'nw')
		self.snoozeMenu.config(width = 10)
		self.snoozeMenu.grid(row=1, pady=5, padx=(9,0), sticky = 'nw')
		self.deleteButton.grid(row = 2, pady=5, padx=(10,0), sticky = 'nw')
	def showSnoozeButton(self):
		self.snoozeButton = tk.Button(self.buttonFrame, text = 'Confirm Snooze', width = 13, command = lambda: self.snoozeRemind())
		self.snoozeButton.grid(row=1, column = 1, pady=5, sticky = 'nw')
	
	def pickedRemind(self):
		#Set the pick date and remind date, change days since, save to csv
		#Delete strain from the listbox self.controller.toDoPage.childPickFrame.snoozeorpick.snoozeVar.set('Snooze')
		self.refineddf = self.controller.toDoPage.childPickFrame.refineddf
		self.idxs = self.controller.toDoPage.childPickFrame.pickListBox.curselection()
		if len(self.idxs) == 1:
			self.idx = int(self.idxs[0])

			self.strainName = self.controller.toDoPage.childPickFrame.names[self.idx]
			self.rowNum = self.pt.model.df.index[self.pt.model.df['Name'] == self.strainName].to_list()[0]

			self.newDatePicked = datetime.date.today()
			self.newDateRemind = self.newDatePicked + datetime.timedelta(days = int(self.pt.model.df.at[self.rowNum,'Maintenance Frequency']))
			#print(self.newDateRemind)
			self.pt.model.df.at[self.rowNum,'Date Picked'] = self.newDatePicked
			self.pt.model.df.at[self.rowNum,'Remind Date'] = self.newDateRemind
			#print('pickedRemind:', id(self.pt.model.df), type(self.pt.model.df))
			self.pt.redraw()

			#self.controller.viewPage.dataWin.refresh()
			#self.controller.saveDatabase() #save to csv
			self.controller.toDoPage.writeTaskEventLog(msg = str(datetime.datetime.now().replace(microsecond = 0, second = 0))+': {} Marked as Picked'.format(self.strainName))

			self.controller.toDoPage.childPickFrame.pickListBox.delete(self.idx)
			self.controller.toDoPage.childPickFrame.names.remove(self.strainName)
			self.refineddf.drop(self.refineddf.index[self.refineddf['Name'] == self.strainName], inplace = True)

	def snoozeRemind(self):
		#Keep the old pick date, set new remind date, keep days since save to csv
		#Delete strain from the listbox
		self.refineddf = self.controller.toDoPage.childPickFrame.refineddf

		self.idxs = self.controller.toDoPage.childPickFrame.pickListBox.curselection()
		if len(self.idxs) == 1:
			self.idx = int(self.idxs[0])

			self.strainName = self.controller.toDoPage.childPickFrame.names[self.idx]
			self.rowNum = self.pt.model.df.index[self.pt.model.df['Name'] == self.strainName].to_list()[0]

			self.newDateRemind = datetime.date.today() + datetime.timedelta(days = int(self.snoozeVar.get()[:1]))
			self.pt.model.df.at[self.rowNum,'Remind Date'] = self.newDateRemind
			#print('snoozeRemind:', id(self.pt.model.df), type(self.pt.model.df))
			self.pt.redraw()
			#self.controller.viewPage.dataWin.refresh()
			#self.controller.saveDatabase() #save to csv
			self.controller.toDoPage.writeTaskEventLog(msg = str(datetime.datetime.now().replace(microsecond = 0, second = 0))+': {} Snoozed for {}'.format(self.strainName, self.snoozeVar.get()))

			self.controller.toDoPage.childPickFrame.pickListBox.delete(self.idx)
			self.controller.toDoPage.childPickFrame.names.remove(self.strainName)
			self.refineddf.drop(self.refineddf.index[self.refineddf['Name'] == self.strainName], inplace = True)

	def deleteRemind(self):

		self.refineddf = self.controller.toDoPage.childPickFrame.refineddf

		self.idxs = self.controller.toDoPage.childPickFrame.pickListBox.curselection()
		if len(self.idxs) == 1:
			self.idx = int(self.idxs[0])

			self.strainName = self.controller.toDoPage.childPickFrame.names[self.idx]
			self.rowNum = self.pt.model.df.index[self.pt.model.df['Name'] == self.strainName].to_list()[0]

			self.pt.model.df.drop(self.refineddf.index[self.refineddf['Name'] == self.strainName], inplace = True)
			#print('deleteRemind:', id(self.pt.model.df), type(self.pt.model.df))
			self.pt.redraw()
			#self.controller.saveDatabase() #save to csv
			self.controller.toDoPage.writeTaskEventLog(msg = str(datetime.datetime.now().replace(microsecond = 0, second = 0))+': {} Deleted from database'.format(self.strainName))

			self.controller.toDoPage.childPickFrame.pickListBox.delete(self.idx)
			self.controller.toDoPage.childPickFrame.names.remove(self.strainName)
			self.refineddf.drop(self.refineddf.index[self.refineddf['Name'] == self.strainName], inplace = True)

###### MENU BAR ########

class MenuBar():
	def __init__(self, parent, controller):

		self.parent = parent 
		self.controller = controller 
		menubar = tk.Menu(parent)

		myMenu = tk.Menu(menubar, tearoff = 0)
		menubar.add_cascade(label = 'Menu', menu = myMenu)
		myMenu.add_command(label = 'About', command = lambda:self.AboutComm())
		myMenu.add_command(label = 'Save Database', command = lambda:self.SaveDBComm())
		myMenu.add_command(label = 'Refresh', command = lambda:self.RefreshComm())
		myMenu.add_separator()
		myMenu.add_command(label = 'Exit', command = lambda:self.ExitComm())
		self.parent.config(menu = menubar)

	def AboutComm(self):
		tk.messagebox.showinfo('Worm Picker', 'Worm Picker is a fun program.')
	
	def SaveDBComm(self):
		self.controller.saveDatabase()
		tk.messagebox.showinfo('Worm Picker', 'Data Saved!')

	def RefreshComm(self):
		self.controller.viewPage.dataWin.refresh()

	def ExitComm(self):
		self.controller.parent.destroy()
		
###### CONTROLLER ######

class ControllerWin(ttk.Frame): #In most cases, parent != controller. Controller references the controller win, 
							   #while parent references the most recent parent frame that the child is in
	def __init__(self, parent):

		ttk.Frame.__init__(self, parent)
		self.parent = parent #parent is the root)


		self.leftFrame = tk.Frame(self.parent)
		self.leftFrame.grid(column = 0, sticky='nesw')
		self.leftFrame.grid_columnconfigure(0, weight=1)
		self.leftFrame.grid_rowconfigure(0, weight=1)

		self.notebook = ttk.Notebook(self.leftFrame) 
		self.notebook.grid(column = 0,sticky = 'nesw')
		self.notebook.grid_columnconfigure(0, weight=1)
		self.notebook.grid_rowconfigure(0, weight = 1)

		self.viewPage = page2(self.notebook, self)
		self.entryPage = page1(self.notebook, self) #Self is the first reference of the omnipotent controller(win)
		self.toDoPage = page3(self.notebook, self)

		menubar = MenuBar(self.parent, self)

	def writeEventLog(self, msg):
		
		numlines = int(self.entryPage.eventLog.index('end - 1 line').split('.')[0])
		self.entryPage.eventLog['state'] = 'normal'
		if numlines==24:
			self.entryPage.eventLog.delete(1.0, 2.0)
		if self.entryPage.eventLog.index('end-1c')!='1.0':
			self.entryPage.eventLog.insert('end', '\n')
		self.entryPage.eventLog.insert('end', msg)
		self.entryPage.eventLog['state'] = 'disabled'

	def enterData(self):


		self.strainEntry = 	self.entryPage.strainvar.strain.get()

		if self.strainEntry == None or self.strainEntry == '':

			logMsg = '{}: No strain entered. Data will not be saved.'.format(datetime.datetime.now().replace(second=0, microsecond=0))
			self.writeEventLog(logMsg)
			return

		else:
			self.pickDateEntry = self.entryPage.pickDatevar.lastPick.get()
			self.constructEntry = 	self.entryPage.constructsvar.constructs.get()
			self.pickEveryEntry = self.entryPage.pickEvery.every.get()
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
						'Notes': self.notesEntry,
						'Remind Date': self.remindDateEntry
					}

			self.addRowtoTable(dataRow)
			self.saveDatabase()

			logMsg = '{}: Saved {} to database'.format(datetime.datetime.now().replace(second=0, microsecond=0), self.strainEntry)

			self.writeEventLog(logMsg) #Write message to appear in log

			self.entryPage.strainvar.strain.delete(0, tk.END)
			self.entryPage.constructsvar.constructs.delete(0, tk.END)
			self.entryPage.pickEvery.every.set(self.entryPage.pickEvery.everyOptions[2])
			self.entryPage.notesvar.notes.delete(0, tk.END)

	def addRowtoTable(self, row):
		self.viewPage.dataWin.pt.model.df = self.viewPage.dataWin.pt.model.df.append(row, ignore_index = True)
		self.viewPage.dataWin.pt.redraw()


	def getData(self):
		self.data = pd.read_csv('WormStrainsData.csv')
		#print('getData:', id(self.data), type(self.data))
		return self.data

	def getStrains(self):
		#Scrape strains that are 'pertinent' from local dataframe, located in the viewWin.
		#return shallow copy
		self.it = self.viewPage.dataWin.pt.model.df.copy(deep = False)
		#print('getStrains:', id(self.it), type(self.it))
		return self.it

	def saveDatabase(self):

		self.viewPage.dataWin.pt.model.df.to_csv('WormStrainsData.csv', index = False)

##### END OF CLASSES #####

def initDB():
	
	if path.exists('WormStrainsData.csv') == False:
		msg = 'Creating database'
		fields = ['Name', 'Date Picked', 'Date Added', 'Strain Type', 'Constructs', 'Experimental Status', 'Maintenance Frequency', 'Notes', 'Remind Date']
		blankrow = ['Example Strain', '2022-01-01', '2022-01-01', 'Array', 'olaEX3847', 'Crossing', '3', 'Delete this row', '2022-01-04']

		with open('WormStrainsData.csv', 'w') as csvfile:
			csvwriter = csv.writer(csvfile)
			csvwriter.writerow(fields)
			csvwriter.writerow(blankrow)
			csvfile.close()

		return msg
	else:
		msg = 'Welcome!'
		return msg


def main():
	initDB()
	root = tk.Tk()
	icon = tk.PhotoImage(file = 'icon.png')
	root.iconphoto(True, icon)
	root.title('Worm Picker Alpha')
	root.geometry('1100x650')
	root.grid_columnconfigure(0, weight = 1)
	ControllerWin(root)
	root.mainloop()


main()