"""
This script handles the gathering of data related to Destiny Players
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
logger = system.util.getLogger("Players")

def getCharacterInfo(membershipType,destinyId,characterIds):
	characterInfo = []
	for characterId in characterIds:
		# Builds the API URL with the base and the actual API path
		apiUrl = apiRoot + "/Destiny2/"+str(membershipType)+"/Profile/"+str(destinyId)+"/Character/"+str(characterId)+"/?components=200"
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
			#print "apiCall " + str(apiCall.url) + " Succeeded, status code: " + str(apiCall.statusCode)
			if len(Response) > 0:
				# If there is any data in the Response dict, do something with it
				#print json.dumps(Response, sort_keys=True, indent=4)
				logger.debug("apiCall " + str(apiCall.url) + " returned a Response")
				#print "apiCall " + str(apiCall.url) + " returned a Response"
				lastOnline = datetime.strptime(Response['character']['data']['dateLastPlayed'], '%Y-%m-%dT%H:%M:%SZ')
				characterInfo.append({"characterid":str(Response['character']['data']['characterId']), "lastOnline":lastOnline})
			else:
				# Move along if the Response dict is empty
				logger.debug("apiCall " + str(apiCall.url) + " returned an empty Response.")
				#print "apiCall " + str(apiCall.url) + " returned an empty Response."
				pass
		else:
			logger.error("apiCall " + str(apiCall.url) + " Failed, status code: " + str(apiCall.statusCode))
			#print "apiCall " + str(apiCall.url) + " Failed, status code: " + str(apiCall.statusCode)
	return system.util.jsonEncode(characterInfo)


def getClanMembers(clanId):
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
				characterInfo = getCharacterInfo(player['destinyUserInfo']['membershipType'],player['destinyUserInfo']['membershipId'],characterIds)
				queryParams = {
					'destinyid':player['destinyUserInfo']['membershipId'],
					'name':player['destinyUserInfo']['displayName'],
					'clanid':player['groupId'],
					'membershiptype':player['destinyUserInfo']['membershipType'],
					'characterids':characterInfo
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
	
# Returns the date the player was last online
def lastOnline(membershiptype,destinyid):
	# Builds the API URL with the base and the actual API path
	apiUrl = apiRoot + "/Destiny2/"+str(membershiptype)+"/Profile/"+str(destinyid)+"/?components=100"
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
		#print "apiCall " + str(apiCall.url) + " Succeeded, status code: " + str(apiCall.statusCode)
		if len(Response) > 0:
			# If there is any data in the Response dict, do something with it
			logger.debug("apiCall " + str(apiCall.url) + " returned a Response")
			#print "apiCall " + str(apiCall.url) + " returned a Response"
			lastOnline = datetime.strptime(Response['profile']['data']['dateLastPlayed'], '%Y-%m-%dT%H:%M:%SZ')
			system.db.runNamedQuery("destiny/players/updateLastOnline", {"playerid":str(destinyid),"lastonline":lastOnline})
			characterInfo = getCharacterInfo(membershiptype,destinyid,Response['profile']['data']['characterIds'])
			system.db.runNamedQuery("destiny/players/updateCharacterLastOnline", {"playerid":str(destinyid),"characterInfo":characterInfo})
		else:
			# Move along if the Response dict is empty
			logger.debug("apiCall " + str(apiCall.url) + " returned an empty Response.")
			#print "apiCall " + str(apiCall.url) + " returned an empty Response."
			pass
	else:
		logger.error("apiCall " + str(apiCall.url) + " Failed, status code: " + str(apiCall.statusCode))
		#print "apiCall " + str(apiCall.url) + " Failed, status code: " + str(apiCall.statusCode)
