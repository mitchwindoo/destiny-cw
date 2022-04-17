# events.py
# Weekly Reset Tuesday @ 1700 UTC
# Daily Reset @ 1700 UTC
# Trials Starts Friday @ 1700 UTC
import calendar
import time
import datetime
logger = system.util.getLogger("Events")
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

def getEventWinners():
	eventDetails = system.dataset.toPyDataSet(system.db.runNamedQuery('destiny/events/getPreviousEvent',{}))[0]
	smallClanWinner = system.dataset.toPyDataSet(system.db.runNamedQuery('destiny/scoring/getEventScore',{'eventScoring':str(eventDetails['scoring_sql']),'eventId':eventDetails['id'],'clanFilter':'AND clans."members" < 25','LIMIT':'LIMIT 1'}))
	mediumClanWinner = system.dataset.toPyDataSet(system.db.runNamedQuery('destiny/scoring/getEventScore',{'eventScoring':str(eventDetails['scoring_sql']),'eventId':eventDetails['id'],'clanFilter':'AND clans."members" > 25 AND clans."members" < 65','LIMIT':'LIMIT 1'}))
	largeClanWinner = system.dataset.toPyDataSet(system.db.runNamedQuery('destiny/scoring/getEventScore',{'eventScoring':str(eventDetails['scoring_sql']),'eventId':eventDetails['id'],'clanFilter':'AND clans."members" > 65','LIMIT':'LIMIT 1'}))
	overallClanWinner = system.dataset.toPyDataSet(system.db.runNamedQuery('destiny/scoring/getEventScore',{'eventScoring':str(eventDetails['scoring_sql']),'eventId':eventDetails['id'],'clanFilter':'AND clans."members" > 0','LIMIT':'LIMIT 1'}))
	try:
		smallClanScore = str(smallClanWinner[0]['game_score'])
		smallClanId = str(smallClanWinner[0]['clanId'])
	except:
		smallClanScore = str(0)
		smallClanId = str(0)
	try:
		mediumClanScore = str(mediumClanWinner[0]['game_score'])
		mediumClanId = str(mediumClanWinner[0]['clanId'])
	except:
		mediumClanScore = str(0)
		mediumClanId = str(0)
	try:
		largeClanScore = str(largeClanWinner[0]['game_score'])
		largeClanId = str(largeClanWinner[0]['clanId'])
	except:
		largeClanScore = str(0)
		largeClanId = str(0)
	
	params = {'event_name':eventDetails['event_name'],
		'eventid':eventDetails['id'],
		'lclan_winner_clanid':largeClanId,
		'lclan_winner_score':largeClanScore,
		'mclan_winner_clanid':mediumClanId,
		'mclan_winner_score':mediumClanScore,
		'sclan_winner_clanid':smallClanId,
		'sclan_winner_score':smallClanScore,
		'overall_winner_clanid':str(overallClanWinner[0]['clanId']),
		'overall_winner_score':str(overallClanWinner[0]['game_score'])}
	system.db.runNamedQuery('destiny/events/addEventWinners',params)

def getCurrentEvent():
	currentEvent = system.dataset.toPyDataSet(system.db.runNamedQuery('destiny/events/getCurrentEvent',{}))
	return currentEvent[0]
	
def getPreviousEvent():
	previousEvent = system.dataset.toPyDataSet(system.db.runNamedQuery('destiny/events/getPreviousEvent',{}))
	return previousEvent[0]
# Tuesday at Reset record Trials / Iron Banner Winners, flush activities.
# Friday at Reset on Non Iron Banner Weeks, record nightfall winners, flush activities.
