# Global Imports
import json
import time
from datetime import datetime
# Global Props
api = system.net.httpClient(redirect_policy="ALWAYS")
apiKey = system.db.runNamedQuery("api/getApiKey", {})
apiRoot = "https://www.bungie.net/Platform"
header = {"X-API-Key":apiKey}
logger = system.util.getLogger("Clans")

			
def addClan(clanId):
	# Returns 1 for Success, 0 for Failure, 2 for Existing
	clanExists = system.db.runNamedQuery('destiny/clans/clanExists', {'clanid':clanId})
	if clanExists == False:
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
				destiny.players.getClanMembers(clanId)
				return 1
			else:
				# Move along if the Response dict is empty
				logger.debug("apiCall " + str(apiCall.url) + " returned an empty Response.")
				print "apiCall " + str(apiCall.url) + " returned an empty Response."
				pass
		else:
			logger.error("apiCall " + str(apiCall.url) + " Failed, status code: " + str(apiCall.statusCode))
			print "apiCall " + str(apiCall.url) + " Failed, status code: " + str(apiCall.statusCode)
			return 0
	else:
		return 2
		
def updateClan(clanId):
	# Returns 1 for Success, 0 for Failure, 2 for Existing
	clanExists = system.db.runNamedQuery('destiny/clans/clanExists', {'clanid':clanId})
	if clanExists == True:
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
				queryPath = 'destiny/clans/updateClan'
				system.db.runNamedQuery(queryPath, queryParams)
				destiny.players.getClanMembers(clanId)
			else:
				# Move along if the Response dict is empty
				logger.debug("apiCall " + str(apiCall.url) + " returned an empty Response.")
				print "apiCall " + str(apiCall.url) + " returned an empty Response."
				pass
		else:
			logger.error("apiCall " + str(apiCall.url) + " Failed, status code: " + str(apiCall.statusCode))
			print "apiCall " + str(apiCall.url) + " Failed, status code: " + str(apiCall.statusCode)
