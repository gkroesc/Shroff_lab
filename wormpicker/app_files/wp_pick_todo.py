'''
Module for viewing picking tasks
'''

#from os import path 
import tkinter as tk
from tkinter import ttk
import datetime
#from pandastable import Table
#import csv
import pandas as pd 
#from tkcalendar import DateEntry
#from ttkthemes import ThemedStyle

#########################################

class Create(ttk.Frame):
	'''
	Page called by main controller window. Anchored in the notebook frame.
	Purpose: Display strains that are in need of attention based on 
	days since last picked and maintenance frequency
	'''
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.parent = parent 
		self.controller = controller

		self.toDoWin = ttk.Frame(self.parent)
		self.toDoWin.grid(sticky='nesw')
		self.toDoWin.grid_columnconfigure(0, weight = 1)
		self.toDoWin.grid_columnconfigure(1, weight = 5)
		
		self.parent.add(self.toDoWin, text='To-Do List', sticky='nesw')

		self.pickBox = ttk.Frame(self.toDoWin, height = 0.85*self.controller.rootHeight)
		self.pickBox.grid(row = 0, column = 0, sticky='nesw', padx = 5, pady = 5, rowspan = 2)

		self.descBox = ttk.LabelFrame(self.toDoWin, text = 'Description', style = 'Header.TLabelframe')
		self.descBox.grid(row = 0, column = 1, sticky='nesw', padx = 5, pady = 5)

		self.weeklyBox = ttk.Frame(self.toDoWin)
		self.weeklyBox.grid(row = 1, column = 1, sticky='nesw', padx = 5, pady = 5)

		self.childPickFrame = pickList(self.pickBox, self.controller)
		self.pickDescFrame = PickDescriptions(self.descBox, self.controller)
		self.weeklyPickFrame = WeeklyPick(self.weeklyBox, self.controller)


class WeeklyPick(ttk.Frame):
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.parent = parent
		self.controller = controller

		self.weeklyPickFrame = ttk.LabelFrame(self.parent, text = 'Weekly Outlook', style = 'Header.TLabelframe')
		self.weeklyPickFrame.pack(expand = True, fill = 'both', padx=5, pady = 5)

		weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
		self.weekdayidx = {}
		#self.weekdaycount = []
		todaywd = datetime.datetime.today().weekday()
		for i in range(todaywd,todaywd+7): #Creates respective list starting at today, ending 6 days from now
			if (i+1) >7:				   #Puts days in order starting with today
				self.weekdayidx[i-7] = 0
			else:
				self.weekdayidx[i] = 0

		self.countsFrame = ttk.Frame(self.weeklyPickFrame)
		self.countsFrame.grid(column = 0, sticky = 'w')
		self.getDayCounts() #Gets weekly counts and overdue count
		myrow = 0
		for key in self.weekdayidx:
			myrow += 1
			if key == 'Overdue':
				ttk.Label(self.countsFrame, text = 'Overdue:').grid(column = 0, row = myrow, sticky = 'e')
				ttk.Label(self.countsFrame, text = self.weekdayidx[key]).grid(column = 1, row = myrow, sticky = 'w')
			else:
				#Day label
				ttk.Label(self.countsFrame, text = weekdays[key]+':').grid(column = 0, row = myrow, sticky = 'e')
				#print(weekdays[key], self.weekdayidx[key])
				
				#Count label
				ttk.Label(self.countsFrame, text = self.weekdayidx[key]).grid(column = 1, row = myrow, sticky = 'w')

		total = 0
		for key in self.weekdayidx:
			total += self.weekdayidx[key]

		self.totalLabel = ttk.Label(self.countsFrame, text = 'Total plates this week: {}'.format(total))
		self.totalLabel.grid(column = 0, columnspan = 2, row = len(self.weekdayidx)+1, sticky = 's', pady = 4)

	def getDayCounts(self):
		pass
		self.df = self.controller.viewPage.dataWin.pt.model.df
		self.df.apply(lambda row: (self.calcCounts(row['Remind Date'])), axis=1)

	def calcCounts(self, remindDate):
		pass
		self.maxDay = (datetime.datetime.today() + datetime.timedelta(weeks=1)).replace(hour = 0, minute = 0, second = 0, microsecond = 0)
		self.minDay = datetime.datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
		dt = self.controller.getDatetime(remindDate)
		if  dt > self.maxDay:
			pass 
		elif dt < self.minDay:
			if 'Overdue' not in self.weekdayidx:
				self.weekdayidx['Overdue'] = 0
				self.weekdayidx['Overdue'] += 1
			else:
				self.weekdayidx['Overdue'] += 1
			
		else:
			self.weekdayidx[dt.weekday()] += 1

class pickList(ttk.Frame):
	'''
	Inner frame structure for to-do list
	Called by page 3 class
	Purpose: Creates nested frame structure that serves as the backbone of 
	the to-do list page.
	Contains template for pick box, descriptions, and interactor buttons. 
	'''
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.parent = parent
		self.controller = controller

		self.refineddf = self.refine()
		self.names = self.refineddf['Name'].tolist()
		self.namesVar = tk.StringVar(value = self.names)

		self.pickListFrame = ttk.Frame(self.parent)
		self.pickListFrame.grid(column = 0, sticky = 'nesw')
		self.pickListFrame.grid_rowconfigure(0, weight = 1)

		self.savepickFrame = ttk.Frame(self.parent)
		self.savepickFrame.grid(column = 0, row = 1, sticky = 'nesw', pady = 5)
		self.savepickButton = ttk.Button(self.savepickFrame, text = 'Save To-Do list', command = lambda: self.savePickList())
		self.savepickButton.pack(expand = True, fill = 'both', padx = (25, 15))
		self.pickListBox = tk.Listbox(self.pickListFrame, height = 25, width = 30, listvariable = self.namesVar, font = (10), selectmode = 'browse', background = self.controller.themeColor)
		self.pickListBox.grid(column = 0, row = 0, sticky = 'nsw', padx=(25,0), pady = (10,0))
		self.pickListBox.bind('<<ListboxSelect>>', lambda a: self.controller.toDoPage.pickDescFrame.descriptions())

		self.vscroll = ttk.Scrollbar(self.pickListFrame, orient= 'vertical', command = self.pickListBox.yview)
		self.vscroll.grid(column = 1, row = 0, sticky = 'nws', padx=(0,15))
		self.pickListBox['yscrollcommand'] = self.vscroll.set

	def savePickList(self):
		savedf = self.refineddf[['Name','Date Picked', 'Strain Type', 
									'Constructs',
									'Location']]
		ls = ['___']*len(savedf)
		savedf.insert(loc = 0, column = 'Status',value = ls, allow_duplicates = True)
		today = str(datetime.date.today())

		dfstring = savedf.to_string(index = False)

		with open('to-do\\to-do_{}.txt'.format(today), 'w') as f:
		    f.write('Strains to maintain for {}\n\n\n'.format(datetime.date.today()))
		    f.write(dfstring)
		    f.close()


		msg = str(datetime.datetime.now().replace(microsecond = 0, second = 0))+": Saved today's to-do list to to-do_{}.txt".format(datetime.date.today())
		self.controller.writeEventLog(msg)

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
		self.df2.drop(labels= ['Date Added','Today'], axis = 1, inplace = True)
		self.df2.fillna('None', inplace = True)

		return self.df2

	def calcDaysSince(self, todayDate, datePicked):
		datePicked = str(datePicked)
		daysSince = todayDate - self.controller.getDatetime(datePicked)
		return daysSince

	def calcDaysUntil(self, todayDate, remindDate):
		#Return boolean if remind date is today?
		remindDate = str(remindDate)
		daysUntil = self.controller.getDatetime(remindDate) - todayDate

		if daysUntil.days < 0: #If daysuntil has passed or is 0
			return True
		else:
			return False



class PickDescriptions(ttk.Frame):

	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.parent = parent
		self.controller = controller




		self.dsmsg = tk.StringVar() #Days since last pick
		self.mfmsg = tk.StringVar() #Picking frequency
		self.dpmsg = tk.StringVar() #date picked
		self.stmsg = tk.StringVar() #strain type
		self.comsg = tk.StringVar() #constructs
		self.exmsg = tk.StringVar() #experimental status
		self.npmsg = tk.StringVar() #Number of plates
		self.lomsg = tk.StringVar() #location
		self.nomsg = tk.StringVar() #notes

		self.dstitle = ttk.Label(self.parent, text = 'Days Since Last Pick:')
		self.mftitle = ttk.Label(self.parent, text = 'Maintenance Frequency (Days):')
		self.dptitle = ttk.Label(self.parent, text = 'Last Date Picked:' )
		self.sttitle = ttk.Label(self.parent, text = 'Strain Type:')
		self.cotitle = ttk.Label(self.parent, text = 'Constructs:')
		self.extitle = ttk.Label(self.parent, text = 'Experimental Status:')
		self.nptitle = ttk.Label(self.parent, text = 'Number of Plates:')
		self.lotitle = ttk.Label(self.parent, text = 'Location')
		self.notitle = ttk.Label(self.parent, text = 'Notes:')

		self.dsdesc = ttk.Label(self.parent, textvariable = self.dsmsg, wraplength = 175, justify = 'left')
		self.mfdesc = ttk.Label(self.parent, textvariable = self.mfmsg, wraplength = 175, justify = 'left')
		self.dpdesc = ttk.Label(self.parent, textvariable = self.dpmsg, wraplength = 175, justify = 'left')
		self.stdesc = ttk.Label(self.parent, textvariable = self.stmsg, wraplength = 175, justify = 'left')
		self.codesc = ttk.Label(self.parent, textvariable = self.comsg, wraplength = 175, justify = 'left')
		self.exdesc = ttk.Label(self.parent, textvariable = self.exmsg, wraplength = 175, justify = 'left')
		self.npdesc = ttk.Label(self.parent, textvariable = self.npmsg, wraplength = 175, justify = 'left')
		self.lodesc = ttk.Label(self.parent, textvariable = self.lomsg, wraplength = 175, justify = 'left')
		self.nodesc = ttk.Label(self.parent, textvariable = self.nomsg, wraplength = 175, justify = 'left')

		self.titles = [self.dstitle, self.mftitle, self.dptitle, self.sttitle, self.cotitle,
						self.extitle, self.nptitle, self.lotitle, self.notitle]
		self.descs = [self.dsdesc, self.mfdesc, self.dpdesc, self.stdesc, self.codesc,
						self.exdesc, self.npdesc, self.lodesc, self.nodesc]

		for i in range(len(self.titles)):
			self.titles[i].grid(row = i, column = 0, sticky = 'ne', pady = 5)
			self.descs[i].grid(row = i, column = 1, sticky = 'nw', pady = 5)


		self.dsmsg.set('')
		self.mfmsg.set('')
		self.dpmsg.set('')
		self.stmsg.set('')
		self.comsg.set('')
		self.exmsg.set('')
		self.npmsg.set('')
		self.lomsg.set('')
		self.nomsg.set('')

		self.snoozeorpick = SnoozePickButtons(self.parent, self.controller)

	def descriptions(self):

		self.refineddf = self.controller.toDoPage.childPickFrame.refineddf
		
		self.idxs = self.controller.toDoPage.childPickFrame.pickListBox.curselection()
		if len(self.idxs) == 1:

			self.idx = int(self.idxs[0])
			
			self.dsmsg.set(self.refineddf['Days Since'].values[self.idx])
			self.mfmsg.set(self.refineddf['Maintenance Frequency'].values[self.idx])
			self.dpmsg.set(self.refineddf['Date Picked'].values[self.idx])
			self.stmsg.set(self.refineddf['Strain Type'].values[self.idx])
			self.comsg.set(self.refineddf['Constructs'].values[self.idx])
			self.exmsg.set(self.refineddf['Experimental Status'].values[self.idx])
			self.npmsg.set(self.refineddf['Number of Plates'].values[self.idx])
			self.lomsg.set(self.refineddf['Location'].values[self.idx])
			self.nomsg.set(self.refineddf['Notes'].values[self.idx])

		self.controller.toDoPage.pickDescFrame.snoozeorpick.snoozeVar.set('Snooze')



class SnoozePickButtons(ttk.Frame):
	'''
	Class called by pickList class in page 3.
	Contains buttons to control interactors with the to-do list
	'''
	def __init__(self, parent, controller):
		ttk.Frame.__init__(self, parent)
		self.parent = parent
		self.controller = controller 
		self.pt = self.controller.viewPage.dataWin.pt
		#print('SnoozePickButtons:', id(self.pt.model.df), type(self.pt.model.df))

		self.buttonFrame = ttk.Frame(self.parent)
		self.buttonFrame.grid(row = 10, column = 0, columnspan=2, sticky = 'w')

		self.pickedButton = ttk.Button(self.buttonFrame, text = 'Mark as Picked', width = 13, command = lambda: self.pickedRemind())

		self.snoozeList = ['Snooze', '1 Day', '2 Days', '3 Days', '4 Days']
		self.snoozeVar = tk.StringVar()

		self.snoozeVar.set(self.snoozeList[0])
		self.snoozeMenu = ttk.OptionMenu(self.buttonFrame, self.snoozeVar, *self.snoozeList, command = lambda x: self.showSnoozeButton())
		self.deleteButton = ttk.Button(self.buttonFrame, text = 'Delete Strain', width = 13, command = lambda: self.deleteRemind())

		self.pickedButton.grid(row=0, pady=5,padx=(10,15), sticky = 'nw')
		self.snoozeMenu.config(width = 10)
		self.snoozeMenu.grid(row=1, pady=5, padx=(9,0), sticky = 'nw')
		self.deleteButton.grid(row = 2, pady=5, padx=(10,0), sticky = 'nw')

	
	def showSnoozeButton(self):
		self.snoozeButton = ttk.Button(self.buttonFrame, text = 'Confirm Snooze', width = 13, command = lambda: self.snoozeRemind())
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
			self.controller.writeEventLog(msg = str(datetime.datetime.now().replace(microsecond = 0, second = 0))+': {} Marked as Picked'.format(self.strainName))

			self.controller.toDoPage.childPickFrame.pickListBox.delete(self.idx)
			self.controller.toDoPage.childPickFrame.names.remove(self.strainName)
			self.refineddf.drop(self.refineddf.index[self.refineddf['Name'] == self.strainName], inplace = True)

		self.controller.saveDatabase()

	def snoozeRemind(self):
		#Keep the old pick date, set new remind date, keep days since save to csv
		#Delete strain from the listbox
		self.refineddf = self.controller.toDoPage.childPickFrame.refineddf
		if self.snoozeVar.get() == 'Snooze':
			return
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
			self.controller.writeEventLog(msg = str(datetime.datetime.now().replace(microsecond = 0, second = 0))+': {} Snoozed for {}'.format(self.strainName, self.snoozeVar.get()))

			self.controller.toDoPage.childPickFrame.pickListBox.delete(self.idx)
			self.controller.toDoPage.childPickFrame.names.remove(self.strainName)
			self.refineddf.drop(self.refineddf.index[self.refineddf['Name'] == self.strainName], inplace = True)

		self.controller.saveDatabase()

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
			self.controller.writeEventLog(msg = str(datetime.datetime.now().replace(microsecond = 0, second = 0))+': {} Deleted from database'.format(self.strainName))

			self.controller.toDoPage.childPickFrame.pickListBox.delete(self.idx)
			self.controller.toDoPage.childPickFrame.names.remove(self.strainName)
			self.refineddf.drop(self.refineddf.index[self.refineddf['Name'] == self.strainName], inplace = True)
		
		self.controller.saveDatabase()
