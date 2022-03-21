# Global Imports
import json
import time
from datetime import datetime
# Global Props
api = system.net.httpClient(redirect_policy="ALWAYS")
apiKey = system.db.runNamedQuery("api/getApiKey", {})
apiRoot = "https://www.bungie.net/Platform"
header = {"X-API-Key":apiKey}
logger = system.util.getLogger("bungieAPI")

# Placeholder with the standard return format for Bungie API calls
def bungieApiCall():
	# Builds the API URL with the base and the actual API path
	apiUrl = apiRoot + "/Destiny2/1/Profile/4611686018432886684/"
	# Performs the HTTP Get using the httpClient set in the Global Props
	apiCall = api.get(url=apiUrl,headers=header)
	# Checks if the response to the httpGet request returned a 200 (Good) value
	if apiCall.good:
		# Response dict standard in Bungie API Calls, returned in a json format.
		Response = apiCall.json['Response']
		# Error Code standard in Bungie API Calls, returned in a json format.
		ErrorCode = int(apiCall.json['ErrorCode'])
		# Throttle Seconds standard in Bungie API Calls, returned in a json format.
		ThrottleSeconds = int(apiCall.json['ThrottleSeconds'])
		# Error Status standard in Bungie API Calls, returned in a json format.
		ErrorStatus = str(apiCall.json['ErrorStatus'])
		# Message Status standard in Bungie API Calls, returned in a json format.
		Message = apiCall.json['Message']
		# Do something if the API Call is successful
		logger.debug("apiCall " + str(apiCall.url) + " Succeeded, status code: " + str(apiCall.statusCode))
		print "apiCall " + str(apiCall.url) + " Succeeded, status code: " + str(apiCall.statusCode)
		if len(Response) > 0:
			# If there is any data in the Response dict, do something with it
			logger.debug("apiCall " + str(apiCall.url) + " returned a Response")
			print "apiCall " + str(apiCall.url) + " returned a Response"
		else:
			# Move along if the Response dict is empty
			logger.debug("apiCall " + str(apiCall.url) + " returned an empty Response.")
			print "apiCall " + str(apiCall.url) + " returned an empty Response."
			pass
	else:
		logger.error("apiCall " + str(apiCall.url) + " Failed, status code: " + str(apiCall.statusCode))
		print "apiCall " + str(apiCall.url) + " Failed, status code: " + str(apiCall.statusCode)

def getPostGameCarnageReport(activityId,destinyMembershipId):
	activityId = str(activityId)
	destinyMembershipId = str(destinyMembershipId)
	apiUrl = apiRoot + "/Destiny2/Stats/PostGameCarnageReport/" + activityId + "/"
	apiCall = api.get(url=apiUrl,headers=header)
	if apiCall.good:
		Response = apiCall.json['Response']
		for entry in Response['entries']:
			if entry['player']['destinyUserInfo']['membershipId'] == destinyMembershipId:
				try:
					pgcr_extended = entry['extended']
				except:
					pgcr_extended = {}
				logger.debug("getPostGameCarnageReport for activity " + activityId + " Completed")
				return {'pgcr_extended':pgcr_extended}
	else:
		logger.error("apiCall " + str(apiCall.url) + " Failed, status code: " + str(apiCall.statusCode))
		print "apiCall " + str(apiCall.url) + " Failed, status code: " + str(apiCall.statusCode)

def ironBanner(membershipType,destinyMembershipId,characterId,queryString="?mode=19&count=5"):
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
				print "ironBanner: activityExists results for Activity ID " + str(activity['activityDetails']['instanceId']) + ": " + str(activityExists)
				if activityExists == False:
					print "ironBanner: Activity ID " + str(activity['activityDetails']['instanceId']) + " does not exist in database"
					logger.debug("ironBanner: Activity ID " + str(activity['activityDetails']['instanceId']) + " does not exist in database")
					timestamp = datetime.strptime(activity['period'], '%Y-%m-%dT%H:%M:%SZ')
					#print type(timestamp)
					# Check if the activity in the returned data is in the current year, keeps the old data from re-populating
					dataCurrent = system.date.isAfter(system.date.parse(timestamp), system.date.addMonths(system.date.now(), -3))
					if dataCurrent == True:
						print "ironBanner: Activity ID " + str(activity['activityDetails']['instanceId']) + " data is being added to the database"
						logger.debug("ironBanner: Activity ID " + str(activity['activityDetails']['instanceId']) + " data is being added to the database")
						pgcr = getPostGameCarnageReport(str(activity['activityDetails']['instanceId']),str(destinyMembershipId))
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
							'avgscoreperkill':activity['values']['averageScorePerKill']['basic']['value'],
							'avgscoreperlife':activity['values']['averageScorePerLife']['basic']['value'],
							'completed':activity['values']['completed']['basic']['displayValue'],
							'completionreason':activity['values']['completionReason']['basic']['displayValue'],
							'deaths':activity['values']['deaths']['basic']['value'],
							'efficiency':activity['values']['efficiency']['basic']['value'],
							'fireteamid':activity['values']['fireteamId']['basic']['displayValue'],
							'kills':activity['values']['kills']['basic']['value'],
							'killsdeathsassists':activity['values']['killsDeathsAssists']['basic']['value'],
							'killsdeathsratio':activity['values']['killsDeathsRatio']['basic']['value'],
							'opponentsdefeated':activity['values']['opponentsDefeated']['basic']['value'],
							'score':activity['values']['score']['basic']['value'],
							'standing':activity['values']['standing']['basic']['displayValue'],
							'team':activity['values']['team']['basic']['value'],
							'teamscore':activity['values']['teamScore']['basic']['value'],
							'timeplayed':activity['values']['timePlayedSeconds']['basic']['displayValue'],
							'pgcr_extended':json.dumps(pgcr['pgcr_extended'])}
						#print queryParams
						queryPath = 'destiny/activities/addActivity'
						system.db.runNamedQuery(queryPath, queryParams)
					else:
						print "ironBanner: Activity ID " + str(activity['activityDetails']['instanceId']) + " being skipped due to age"
						logger.debug("ironBanner: Activity ID " + str(activity['activityDetails']['instanceId']) + " being skipped due to age")
				else:
					print "ironBanner: Activity ID " + str(activity['activityDetails']['instanceId']) + " Has already been logged to the database"
					logger.debug("ironBanner: Activity ID " + str(activity['activityDetails']['instanceId']) + " Has already been logged to the database")
			else:
				print "No Response in apiCall, ErrorCode: " + str(ErrorCode) + ", ThrottleSeconds: " + str(ThrottleSeconds) + ", ErrorStatus: " + str(ErrorStatus) + ", Message: " + str(Message)
				logger.debug("No Response in apiCall " + str(apiCall.url) + ", ErrorCode: " + str(ErrorCode) + ", ThrottleSeconds: " + str(ThrottleSeconds) + ", ErrorStatus: " + str(ErrorStatus) + ", Message: " + str(Message))
				
	else:
		logger.error("apiCall " + str(apiCall.url) + "  Failed, status code: " + str(apiCall.statusCode))
		print "apiCall " + str(apiCall.url) + "  Failed, status code: " + str(apiCall.statusCode)
			
def syncIronBanner():
	startTime = time.time()
	queryParams = {}
	#print queryParams
	queryPath = 'destiny/clans/getAllPlayers'
	playerList = system.dataset.toPyDataSet(system.db.runNamedQuery(queryPath, queryParams))
	
	for player in playerList:
		characters = json.loads(player['characterids'])
		for i in characters:
			ironBanner(player['membershiptype'],player['destinyid'],i,"?mode=19&count=5")
	executionTime = (time.time() - startTime)
	system.db.runNamedQuery("api/scriptLogs", {"script":"syncIronBanner","script_runtime":executionTime})
	print "syncIronBanner Script completed in " + str(executionTime) + " seconds"
	logger.info("syncIronBanner Script completed in " + str(executionTime) + " seconds")

def resetIronBanner():
	startTime = time.time()
	system.db.runNamedQuery('destiny/activities/deleteAllActivities', {})
	queryParams = {}
	#print queryParams
	queryPath = 'destiny/clans/getAllPlayers'
	playerList = system.dataset.toPyDataSet(system.db.runNamedQuery(queryPath, queryParams))
	
	for player in playerList:
		characters = json.loads(player['characterids'])
		for i in characters:
			ironBanner(player['membershiptype'],player['destinyid'],i,"?mode=19")
	executionTime = (time.time() - startTime)
	system.db.runNamedQuery("api/scriptLogs", {"script":"syncIronBanner","script_runtime":executionTime})
	print "resetIronBanner Script completed in " + str(executionTime) + " seconds"
	logger.info("resetIronBanner Script completed in " + str(executionTime) + " seconds")
