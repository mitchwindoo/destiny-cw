# events.py
# Weekly Reset Tuesday @ 1700 UTC
# Daily Reset @ 1700 UTC
# Trials Starts Friday @ 1700 UTC
import calendar
import time
import datetime
logger = system.util.getLogger("events")
currentTimestamp = system.date.now()

# Weekly on Reset -- Update the Event Dates in the Database
def updateEventTimes():
	current_time = datetime.datetime.now()
	# Build the timestamps for event switchovers
	friday_base = datetime.datetime.combine((current_time.date() - datetime.timedelta(days=current_time.weekday()) + datetime.timedelta(days=4, weeks=0)), datetime.time(17))
	friday = system.date.fromMillis(calendar.timegm(time.strptime(str(friday_base) + " UTC", '%Y-%m-%d %H:%M:%S UTC'))*1000)
	tuesday_base = datetime.datetime.combine((current_time.date() - datetime.timedelta(days=current_time.weekday()) + datetime.timedelta(days=1, weeks=0)), datetime.time(17))
	tuesday = system.date.fromMillis(calendar.timegm(time.strptime(str(tuesday_base) + " UTC", '%Y-%m-%d %H:%M:%S UTC'))*1000)
	# Upcoming Events to Database
	ibStartDate = system.date.parse('2022-04-12 17:00 UTC', 'yyyy-MM-dd HH:mm z')
	ibEndDate = system.date.parse('2022-04-19 17:00 UTC', 'yyyy-MM-dd HH:mm z')
	nightfallStartDate = tuesday
	nightfallEndDate = friday
	trialsStartDate = friday
	trialsEndDate = system.date.addWeeks(tuesday,1)
	system.db.runNamedQuery('destiny/events/updateEventDates', {'eventName':'Iron Banner','startDate':ibStartDate,'endDate':ibEndDate})
	system.db.runNamedQuery('destiny/events/updateEventDates', {'eventName':'Nightfall','startDate':nightfallStartDate,'endDate':nightfallEndDate})
	system.db.runNamedQuery('destiny/events/updateEventDates', {'eventName':'Trials of Osiris','startDate':trialsStartDate,'endDate':trialsEndDate})

def getEventWinners(eventName):
	smallClanWinner = system.dataset.toPyDataSet(system.db.runNamedQuery('destiny/activities/getSmallClanActivityScore',{}))
	mediumClanWinner = system.dataset.toPyDataSet(system.db.runNamedQuery('destiny/activities/getMediumClanActivityScore',{}))
	largeClanWinner = system.dataset.toPyDataSet(system.db.runNamedQuery('destiny/activities/getLargeClanActivityScore',{}))
	overallClanWinner = system.dataset.toPyDataSet(system.db.runNamedQuery('destiny/activities/getTotalActivityScore',{}))
	params = {'event_name':eventName,
		'lclan_winner_clanid':str(largeClanWinner[0]['clanid']),
		'lclan_winner_score':str(largeClanWinner[0]['score']),
		'mclan_winner_clanid':str(mediumClanWinner[0]['clanid']),
		'mclan_winner_score':str(mediumClanWinner[0]['score']),
		'sclan_winner_clanid':str(smallClanWinner[0]['clanid']),
		'sclan_winner_score':str(smallClanWinner[0]['score']),
		'overall_winner_clanid':str(overallClanWinner[0]['clanid']),
		'overall_winner_score':str(overallClanWinner[0]['score'])}
	system.db.runNamedQuery('destiny/events/addEventWinners',params)

def getCurrentEvent(currentTimestamp):
	currentEvents = system.dataset.toPyDataSet(system.db.runNamedQuery('destiny/events/getCurrentEvents',{}))
	if system.date.isBetween(currentTimestamp,currentEvents[0]['start_date'],currentEvents[0]['end_date']):
		return {'eventName':'Iron Banner', 'mode':19}
	elif system.date.isBetween(currentTimestamp,currentEvents[1]['start_date'],currentEvents[1]['end_date']):
		return {'eventName':'Nightfall', 'mode':46}
	elif system.date.isBetween(currentTimestamp,currentEvents[2]['start_date'],currentEvents[2]['start_date']):
		return {'eventName':'Trials of Osiris', 'mode':84}

# Tuesday at Reset record Trials / Iron Banner Winners, flush activities.
# Friday at Reset on Non Iron Banner Weeks, record nightfall winners, flush activities.
