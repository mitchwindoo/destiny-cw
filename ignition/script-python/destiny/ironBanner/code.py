# Global Imports
import json
import time
from datetime import datetime

logger = system.util.getLogger("ironBanner")

def update():
	startTime = time.time()
	queryParams = {}
	logger.info("destiny.ironBanner.update Started")
	#print queryParams
	queryPath = 'destiny/clans/getAllPlayers'
	playerList = system.dataset.toPyDataSet(system.db.runNamedQuery(queryPath, queryParams))
	for player in playerList:
		characters = json.loads(player['characterids'])
		for i in characters:
			destiny.activities.getActivities(player['membershiptype'],player['destinyid'],i,"?mode=19&count=5")
	executionTime = (time.time() - startTime)
	system.db.runNamedQuery("api/scriptLogs", {"script":"destiny.ironBanner.update","script_runtime":executionTime})
	print "destiny.ironBanner.update Script completed in " + str(executionTime) + " seconds"
	logger.info("destiny.ironBanner.update Script completed in " + str(executionTime) + " seconds")

def fullSync():
	startTime = time.time()
	queryParams = {}
	logger.info("destiny.ironBanner.fullSync Started")
	#print queryParams
	queryPath = 'destiny/clans/getAllPlayers'
	playerList = system.dataset.toPyDataSet(system.db.runNamedQuery(queryPath, queryParams))
	for player in playerList:
		characters = json.loads(player['characterids'])
		for i in characters:
			destiny.activities.getActivities(player['membershiptype'],player['destinyid'],i,"?mode=19")
	executionTime = (time.time() - startTime)
	system.db.runNamedQuery("api/scriptLogs", {"script":"destiny.ironBanner.fullSync","script_runtime":executionTime})
	print "destiny.ironBanner.fullSync Script completed in " + str(executionTime) + " seconds"
	logger.info("destiny.ironBanner.fullSync Script completed in " + str(executionTime) + " seconds")

def reset():
	startTime = time.time()
	logger.info("destiny.ironBanner.reset Started")
	system.db.runNamedQuery('destiny/activities/deleteAllActivities', {})
	queryParams = {}
	#print queryParams
	queryPath = 'destiny/clans/getAllPlayers'
	playerList = system.dataset.toPyDataSet(system.db.runNamedQuery(queryPath, queryParams))
	
	for player in playerList:
		characters = json.loads(player['characterids'])
		for i in characters:
			destiny.activities.getActivities(player['membershiptype'],player['destinyid'],i,"?mode=19")
	executionTime = (time.time() - startTime)
	system.db.runNamedQuery("api/scriptLogs", {"script":"destiny.ironBanner.reset","script_runtime":executionTime})
	print "destiny.ironBanner.reset Script completed in " + str(executionTime) + " seconds"
	logger.info("destiny.ironBanner.reset Script completed in " + str(executionTime) + " seconds")
