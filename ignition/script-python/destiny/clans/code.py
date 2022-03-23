# Global Imports
import json
import time
from datetime import datetime
# Global Props
api = system.net.httpClient(redirect_policy="ALWAYS")
apiKey = system.db.runNamedQuery("api/getApiKey", {})
apiRoot = "https://www.bungie.net/Platform"
header = {"X-API-Key":apiKey}
logger = system.util.getLogger("clans")

def getPlayers(clanId):
	startTime = time.time()
	## Generic API Information
	apiPath = apiRoot + "/GroupV2/" + str(clanId) + "/Members/"
	apiCall = json.loads(system.net.httpGet(apiPath,headerValues=header))
	Response = apiCall['Response']
	ErrorCode = int(apiCall['ErrorCode'])
	ThrottleSeconds = int(apiCall['ThrottleSeconds'])
	ErrorStatus = str(apiCall['ErrorStatus'])
	Message = apiCall['Message']
	## Debug
	#print json.dumps(Response['results'], indent=4, sort_keys=True)
	## Specific Script Properties
	players = Response['results']
	for player in players:
		## Check if Player is already in the Database by Destiny ID
		queryParams = {'destinyid':player['destinyUserInfo']['membershipId']}
		queryPath = 'destiny/clans/playerExists'
		memberExists = system.db.runNamedQuery(queryPath, queryParams)
		## If the player does not exist, add them to the Database
		if memberExists == False:
			try:
				characterIds = json.loads(system.net.httpGet(apiRoot + "/Destiny2/" + str(player['destinyUserInfo']['membershipType']) + "/Profile/" + str(player['destinyUserInfo']['membershipId']) + "/?components=100",headerValues=header))['Response']['profile']['data']['characterIds']
				queryParams = {
					'destinyid':player['destinyUserInfo']['membershipId'],
					'name':player['destinyUserInfo']['displayName'],
					'clanid':player['groupId'],
					'membershiptype':player['destinyUserInfo']['membershipType'],
					'characterids':json.dumps(characterIds)
					}
				queryPath = 'destiny/clans/addPlayers'
				system.db.runNamedQuery(queryPath, queryParams)
				logger.debug("Added " + str(player['destinyUserInfo']['displayName']) + " To Player Database")
			except:
				logger.error("Unable to Locate Player Account for ID " + player['destinyUserInfo']['membershipId'])
				pass
		else:
			logger.info(str(player['destinyUserInfo']['displayName']) + " Already Exists in Database")
	executionTime = (time.time() - startTime)
	logger.info("getPlayers for Clan ID " + str(clanId) + " Script completed in " + str(executionTime) + " seconds")
			
def addClan(clanId):
	# Builds the API URL with the base and the actual API path
	apiUrl = apiRoot + "/GroupV2/" + str(clanId) + "/"
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
			#print json.dumps(Response, indent=4, sort_keys=True)
			queryParams = {
				'clanId':clanId,
				'clanName':str(Response['detail']['name']),
				'clanFounder':str(Response['founder']['bungieNetUserInfo']['supplementalDisplayName']),
				'clanFounderBungieId':str(Response['founder']['bungieNetUserInfo']['membershipId']),
				'clanFounderDestinyId':str(Response['founder']['destinyUserInfo']['membershipId']),
				'clanAbout':str(Response['detail']['about']),
				'clanMembers':int(Response['detail']['memberCount']),
				'clanMotto':str(Response['detail']['motto']),
				'clanCallsign':str(Response['detail']['clanInfo']['clanCallsign'])}
			queryPath = 'destiny/clans/addClan'
			system.db.runNamedQuery(queryPath, queryParams)
			getPlayers(clanId)
		else:
			# Move along if the Response dict is empty
			logger.debug("apiCall " + str(apiCall.url) + " returned an empty Response.")
			print "apiCall " + str(apiCall.url) + " returned an empty Response."
			pass
	else:
		logger.error("apiCall " + str(apiCall.url) + " Failed, status code: " + str(apiCall.statusCode))
		print "apiCall " + str(apiCall.url) + " Failed, status code: " + str(apiCall.statusCode)
