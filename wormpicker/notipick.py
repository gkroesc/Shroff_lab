"""
Wormpicker.py supplement
Notifications
"""

from os import path
import datetime #for reading present date
import time 
from plyer import notification #for getting notification on your PC
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

def remindBool(date):
	todayDate = datetime.datetime.today().replace(minute=0, hour=0, second=0, microsecond=0)

	try:
		daysUntil = datetime.datetime.strptime(date, '%Y-%m-%d') - todayDate

	except ValueError:
		try:
			daysUntil = datetime.datetime.strptime(date, '%Y/%m/%d') - todayDate
		except ValueError:
			try:
				daysUntil = datetime.datetime.strptime(date, '%m-%d-%Y') - todayDate
			except ValueError:
				try:
					daysUntil = datetime.datetime.strptime(date, '%m/%d/%Y') - todayDate
				except ValueError:
					try:
						daysUntil = datetime.datetime.strptime(date, '%d-%m-%Y') - todayDate
					except ValueError:
						try:
							daysUntil = datetime.datetime.strptime(date, '%d/%m/%Y') - todayDate
						except ValueError:
							return None

	if daysUntil.days <= 0: #If daysuntil has passed or is 0
		return True
	else:
		return False


def main():
	if path.exists('WormStrainsData.csv') != True:
		print('File does not yet exist. Please run wormpicker.py first!')
		quit()

	while True:
		data = pd.read_csv('WormStrainsData.csv')
		df = data[['Name','Date Picked', 'Remind Date']]

		df['RemindBool'] = df.apply(lambda row: remindBool(row['Remind Date']), axis = 1)
		
		finaldf = df[df['RemindBool'] == True]
		lsdf = finaldf.values.tolist()
		notifMsg = 'Number of Strains to pick: {}\n'.format(len(lsdf))

		for minilist in lsdf:
			if len(notifMsg) >75:
				break
			msg = '{}: Last picked on {}'.format(minilist[0], minilist[1]) #{Name} last picked on {date picked}
			notifMsg += msg+'\n'

			notifMsg += 'Open Worm Picker to view all notifications'
		notification.notify(title = 'Worm Picker', 
							message = notifMsg,
							app_icon = 'icon.ico',
							)
							

		time.sleep(60*60) #<-- every hour notification
							
	
main()