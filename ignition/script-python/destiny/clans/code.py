# Global Imports
import json
# Global Props
apiKey = system.db.runNamedQuery("api/getApiKey", {})
apiRoot = "https://www.bungie.net/Platform"
header = {"X-API-Key":apiKey}
logger = system.util.getLogger("bungieAPI")

def getPlayers(clanId):
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
				logger.info("Added " + str(player['destinyUserInfo']['displayName']) + " To Player Database")
				print "Added " + str(player['destinyUserInfo']['displayName']) + " To Player Database"
			except:
				logger.error("Unable to Locate Player Account for ID " + player['destinyUserInfo']['membershipId'])
				print "Unable to Locate Player Account for ID " + player['destinyUserInfo']['membershipId']
				pass
		else:
			logger.info(str(player['destinyUserInfo']['displayName']) + " Already Exists in Database")
			print str(player['destinyUserInfo']['displayName']) + " Already Exists in Database"
			
def addClan(clanId):
	apiPath = apiRoot + "/GroupV2/" + str(clanId) + "/"
	apiCall = json.loads(system.net.httpGet(apiPath,headerValues=header))
	Response = apiCall['Response']
	ErrorCode = int(apiCall['ErrorCode'])
	ThrottleSeconds = int(apiCall['ThrottleSeconds'])
	ErrorStatus = str(apiCall['ErrorStatus'])
	Message = apiCall['Message']
	## Debug
	#print json.dumps(Response, indent=4, sort_keys=True)
	clanId = clanId
	clanName = str(Response['detail']['name'])
	clanFounder = str(Response['founder']['bungieNetUserInfo']['supplementalDisplayName'])
	clanFounderBungieId = long(Response['founder']['bungieNetUserInfo']['membershipId'])
	clanFounderDestinyId = long(Response['founder']['destinyUserInfo']['membershipId'])
	clanAbout = str(Response['detail']['about'])
	clanMembers = int(Response['detail']['memberCount'])
	clanMotto = str(Response['detail']['motto'])
	# Write Values to the Database
	queryParams = {'clanId':clanId,'clanName':clanName,'clanFounder':clanFounder,'clanFounderBungieId':clanFounderBungieId,'clanFounderDestinyId':clanFounderDestinyId,'clanAbout':clanAbout,'clanMembers':clanMembers,'clanMotto':clanMotto}
	queryPath = 'destiny/clans/addClan'
	system.db.runNamedQuery(queryPath, queryParams)
