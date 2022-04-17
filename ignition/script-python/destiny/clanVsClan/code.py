"""
This script handles the gathering of data related to Destiny Activities, and their corosponding Post Game Carnage Report (PGCR).
This script specifically records clan vs clan matches.
PrivateMatchesAll: 32, PrivateMatchesClash: 51, PrivateMatchesControl: 52, PrivateMatchesSupremacy: 53, PrivateMatchesCountdown: 54, PrivateMatchesSurvival: 55, PrivateMatchesMayhem: 56, PrivateMatchesRumble: 57
"""

# Global Imports
import json
import time
from datetime import datetime
# Global Props
api = system.net.httpClient(redirect_policy="ALWAYS")
apiKey = system.db.runNamedQuery("api/getApiKey", {})
apiRoot = "https://www.bungie.net/Platform"
header = {"X-API-Key":apiKey}
logger = system.util.getLogger("ClanVsClanActivities")

def getPostGameCarnageReport(activityId,destinyMembershipId):
	activityId = str(activityId)
	destinyMembershipId = str(destinyMembershipId)
	clanId = system.dataset.toPyDataSet(system.db.runNamedQuery("destiny/clans/getPlayerInfo", {'destinyid':destinyMembershipId}))[0]['clanid']
	clanBonus = 0
	clanMembers = []
	playerList = []
	apiUrl = apiRoot + "/Destiny2/Stats/PostGameCarnageReport/" + activityId + "/"
	apiCall = api.get(url=apiUrl,headers=header)
	if apiCall.good:
		Response = apiCall.json['Response']
		#print json.dumps(Response, indent=4, sort_keys=True)
		for entry in Response['entries']:
			#print json.dumps(entry, indent=4, sort_keys=True)
			#print entry['player']['destinyUserInfo']['membershipId']
			if entry['player']['destinyUserInfo']['membershipId'] == destinyMembershipId:
				try:
					pgcr_extended = entry['extended']
				except:
					pgcr_extended = {}
				logger.debug("getPostGameCarnageReport for activity " + activityId + " Completed")
			else:
				clanMember = system.db.runNamedQuery("destiny/clans/getClanMatch", {'playerid':str(entry['player']['destinyUserInfo']['membershipId']),'clanid':str(clanId)})
				clanMembers.append(bool(clanMember))
				playerList.append(system.db.runNamedQuery("destiny/clans/playerExists", {'destinyid':str(entry['player']['destinyUserInfo']['membershipId'])}))
				if clanMember == 1:
					clanBonus = clanBonus + 0.05
		if clanBonus > 0.25:
			clanBonus = 1.25
		else:
			clanBonus = clanBonus + 1
		if all(playerList) and not all(clanMembers):
			valid_clanvclan = True
		else:
			valid_clanvclan = False
		return {'pgcr_extended':pgcr_extended,'clan_bonus':clanBonus,'started_from_beginning':Response['activityWasStartedFromBeginning'], 'valid_clanvclan':valid_clanvclan}
	else:
		logger.error("apiCall " + str(apiCall.url) + " Failed, status code: " + str(apiCall.statusCode))
		#print "apiCall " + str(apiCall.url) + " Failed, status code: " + str(apiCall.statusCode)

def getActivities(membershipType,destinyMembershipId,characterId,queryString):
	apiUrl = apiRoot + "/Destiny2/" + str(membershipType) + "/Account/" + str(destinyMembershipId) + "/Character/" + str(characterId) + "/Stats/Activities/" + queryString
	apiCall = api.get(url=apiUrl,headers=header)
	if apiCall.good:
		Response = apiCall.json['Response']
		ErrorCode = int(apiCall.json['ErrorCode'])
		ThrottleSeconds = int(apiCall.json['ThrottleSeconds'])
		ErrorStatus = str(apiCall.json['ErrorStatus'])
		Message = apiCall.json['Message']
		## Debug
		#print json.dumps(apiCall, indent=4, sort_keys=True)
		#system.db.runNamedQuery("destiny/activities/deleteAllActivities", {})
		#print destinyMembershipId
		## Specific Script Properties
		#print len(Response)
		if len(Response) > 0:
			activities = Response['activities']
			#print activities
			for activity in activities:
				# Check if the activity has already been recorded in the Database
				queryParams = {'playerdestinyid':str(destinyMembershipId),'instanceid':str(activity['activityDetails']['instanceId'])}
				queryPath = 'destiny/activities/activityExists'
				activityExists = system.db.runNamedQuery(queryPath, queryParams)
				logger.debug("ironBanner: activityExists results for Activity ID " + str(activity['activityDetails']['instanceId']) + ": " + str(activityExists))
				#print "ironBanner: activityExists results for Activity ID " + str(activity['activityDetails']['instanceId']) + ": " + str(activityExists)
				if activityExists == False:
					#print "ironBanner: Activity ID " + str(activity['activityDetails']['instanceId']) + " does not exist in database"
					logger.debug("ironBanner: Activity ID " + str(activity['activityDetails']['instanceId']) + " does not exist in database")
					timestamp = datetime.strptime(activity['period'], '%Y-%m-%dT%H:%M:%SZ')
					#print type(timestamp)
					# Check if the activity in the returned data is in the current week, keeps the old data from re-populating
					dataCurrent = system.date.isAfter(system.date.parse(timestamp), system.date.addWeeks(system.date.now(), -1))
					#dataCurrent = True
					if dataCurrent == True:
						#print "ironBanner: Activity ID " + str(activity['activityDetails']['instanceId']) + " data is being added to the database"
						logger.debug("ironBanner: Activity ID " + str(activity['activityDetails']['instanceId']) + " data is being added to the database")
						try: 
							pgcr = getPostGameCarnageReport(str(activity['activityDetails']['instanceId']),str(destinyMembershipId))
						except:
							logger.error("Failed to get PGCR on " + str(activity['activityDetails']['instanceId']) + ", PlayerId: " + str(destinyMembershipId))
							pgcr = {'pgcr_extended':{},'clan_bonus':1,'started_from_beginning':False,'valid_clanvclan':False}
						try:
							standing = activity['values']['standing']['basic']['displayValue']
						except:
							standing = 'NA'
						# If the match was played against another registered clan, record the match.
						if pgcr['valid_clanvclan'] == True:
							# Write Values to the Database
							queryParams = {'playercharacterid':str(characterId),
							'playerdestinyid':str(destinyMembershipId),
							'instanceid':activity['activityDetails']['instanceId'],
							'modes':json.dumps(activity['activityDetails']['modes']),
							'mode':activity['activityDetails']['mode'],
							'isprivate':activity['activityDetails']['isPrivate'],
							'referenceid':activity['activityDetails']['referenceId'],
							'timestamp':timestamp,
							'activityduration':activity['values']['activityDurationSeconds']['basic']['displayValue'],
							'assists':activity['values']['assists']['basic']['value'],
							'completed':activity['values']['completed']['basic']['displayValue'],
							'completed_value':activity['values']['completed']['basic']['value'],
							'completionreason':activity['values']['completionReason']['basic']['displayValue'],
							'deaths':activity['values']['deaths']['basic']['value'],
							'efficiency':activity['values']['efficiency']['basic']['value'],
							'fireteamid':activity['values']['fireteamId']['basic']['displayValue'],
							'kills':activity['values']['kills']['basic']['value'],
							'killsdeathsassists':activity['values']['killsDeathsAssists']['basic']['value'],
							'killsdeathsratio':activity['values']['killsDeathsRatio']['basic']['value'],
							'opponentsdefeated':activity['values']['opponentsDefeated']['basic']['value'],
							'score':activity['values']['score']['basic']['value'],
							'standing':standing,
							'team':activity['values']['team']['basic']['value'],
							'teamscore':activity['values']['teamScore']['basic']['value'],
							'timeplayed':activity['values']['timePlayedSeconds']['basic']['displayValue'],
							'timeplayed_seconds':activity['values']['timePlayedSeconds']['basic']['value'],
							'pgcr_extended':json.dumps(pgcr['pgcr_extended']),
							'clan_bonus':pgcr['clan_bonus'],
							'start_seconds':activity['values']['startSeconds']['basic']['value'],
							'started_from_beginning':pgcr['started_from_beginning']}
							#print queryParams
							queryPath = 'destiny/activities/addActivity'
							system.db.runNamedQuery(queryPath, queryParams)
					else:
						#print "ironBanner: Activity ID " + str(activity['activityDetails']['instanceId']) + " being skipped due to age"
						logger.debug("Activity ID " + str(activity['activityDetails']['instanceId']) + " being skipped due to age")
				else:
					#print "ironBanner: Activity ID " + str(activity['activityDetails']['instanceId']) + " Has already been logged to the database"
					logger.debug("Activity ID " + str(activity['activityDetails']['instanceId']) + " Has already been logged to the database")
			else:
				#print "No Response in apiCall, ErrorCode: " + str(ErrorCode) + ", ThrottleSeconds: " + str(ThrottleSeconds) + ", ErrorStatus: " + str(ErrorStatus) + ", Message: " + str(Message)
				logger.debug("No Response in apiCall " + str(apiCall.url) + ", ErrorCode: " + str(ErrorCode) + ", ThrottleSeconds: " + str(ThrottleSeconds) + ", ErrorStatus: " + str(ErrorStatus) + ", Message: " + str(Message))
				
	else:
		logger.error("apiCall " + str(apiCall.url) + "  Failed, status code: " + str(apiCall.statusCode))
		#print "apiCall " + str(apiCall.url) + "  Failed, status code: " + str(apiCall.statusCode)

def updateActivities(mode):
	batchSize = 25
	delayTime = 10
	startTime = time.time()
	logger.info("destiny.activities.update Started")
	system.tag.writeBlocking(["[default]UpdateInProgress"],[True])
	activePlayerList = system.dataset.toPyDataSet(system.db.runNamedQuery("destiny/players/getActivePlayers", {}))
	characterList = []
	for player in activePlayerList:
		characters = json.loads(player['characterids'])
		for character in characters:
			recentlyOnline = system.date.isAfter(system.date.parse(character['lastOnline']), system.date.addHours(system.date.now(), -2))
			if recentlyOnline == True:
				characterList.append({'membershiptype':player['membershiptype'],'destinyid':str(player['destinyid']),'characterid':str(character['characterid']),'queryString':"?mode="+str(mode)+"&count=10"})
	while characterList:
		batch = characterList[:batchSize]
		print batch
		for i in batch:
			def updateActivities():
				destiny.clanVsClan.getActivities(i['membershiptype'],i['destinyid'],i['characterid'],i['queryString'])
			thread = system.util.invokeAsynchronous(updateActivities)
			logger.debug(str(thread))
		characterList = characterList[batchSize:]
		time.sleep(delayTime)
	executionTime = (time.time() - startTime)
	system.db.runNamedQuery("api/scriptLogs", {"script":"destiny.activities.update","script_runtime":executionTime})
	print "destiny.activities.update Script completed in " + str(executionTime) + " seconds"
	system.tag.writeBlocking(["[default]UpdateInProgress"],[False])
	logger.info("destiny.activities.update Script completed in " + str(executionTime) + " seconds")
		
def fullSyncActivities(mode):
	batchSize = 10
	delayTime = 30
	startTime = time.time()
	logger.info("destiny.activities.fullSyncActivities Started")
	system.tag.writeBlocking(["[default]UpdateInProgress"],[True])
	activePlayerList = system.dataset.toPyDataSet(system.db.runNamedQuery("destiny/players/getActivePlayers", {}))
	characterList = []
	for player in activePlayerList:
		characters = json.loads(player['characterids'])
		for character in characters:
			recentlyOnline = system.date.isAfter(system.date.parse(character['lastOnline']), system.date.addHours(system.date.now(), -48))
			if recentlyOnline == True:
				characterList.append({'membershiptype':player['membershiptype'],'destinyid':str(player['destinyid']),'characterid':str(character['characterid']),'queryString':"?mode="+str(mode)})
	while characterList:
		batch = characterList[:batchSize]
		print batch
		for i in batch:
			def updateActivities():
				destiny.clanVsClan.getActivities(i['membershiptype'],i['destinyid'],i['characterid'],i['queryString'])
			thread = system.util.invokeAsynchronous(updateActivities)
			logger.debug(str(thread))
		characterList = characterList[batchSize:]
		time.sleep(delayTime)
	executionTime = (time.time() - startTime)
	system.db.runNamedQuery("api/scriptLogs", {"script":"destiny.activities.fullSync","script_runtime":executionTime})
	print "destiny.activities.fullSync Script completed in " + str(executionTime) + " seconds"
	system.tag.writeBlocking(["[default]UpdateInProgress"],[False])
	logger.info("destiny.activities.fullSync Script completed in " + str(executionTime) + " seconds")
