# Global Imports
import json
from datetime import datetime
# Global Props
apiKey = system.db.runNamedQuery("api/getApiKey", {})
apiRoot = "https://www.bungie.net/Platform"
header = {"X-API-Key":apiKey}
logger = system.util.getLogger("bungieAPI")

def ironBanner(membershipType,destinyMembershipId,characterId):
	apiPath = apiRoot + "/Destiny2/" + str(membershipType) + "/Account/" + str(destinyMembershipId) + "/Character/" + str(characterId) + "/Stats/Activities/?mode=19"
	try:
		apiCall = json.loads(system.net.httpGet(apiPath,headerValues=header))
		Response = apiCall['Response']
		ErrorCode = int(apiCall['ErrorCode'])
		ThrottleSeconds = int(apiCall['ThrottleSeconds'])
		ErrorStatus = str(apiCall['ErrorStatus'])
		Message = apiCall['Message']
		## Debug
		#print json.dumps(Response['activities'], indent=4, sort_keys=True)
		#system.db.runNamedQuery("destiny/activities/deleteAllActivities", {})
		#print destinyMembershipId
		## Specific Script Properties
		if len(Response) > 0:
			activities = Response['activities']
			for activity in activities:
				# Check if the activity has already been recorded in the Database
				queryParams = {'playerdestinyid':destinyMembershipId,'instanceid':activity['activityDetails']['instanceId']}
				queryPath = 'destiny/activities/activityExists'
				activityExists = system.db.runNamedQuery(queryPath, queryParams)
				if activityExists == False:
					# Write Values to the Database
					queryParams = {'playercharacterid':str(characterId),'playerdestinyid':str(destinyMembershipId),'instanceid':activity['activityDetails']['instanceId'],'modes':json.dumps(activity['activityDetails']['modes']),'mode':activity['activityDetails']['mode'],'isprivate':activity['activityDetails']['isPrivate'],'referenceid':activity['activityDetails']['referenceId'],'timestamp':datetime.strptime(activity['period'], '%Y-%m-%dT%H:%M:%SZ'),'activityduration':activity['values']['activityDurationSeconds']['basic']['displayValue'],'assists':activity['values']['assists']['basic']['value'],'avgscoreperkill':activity['values']['averageScorePerKill']['basic']['value'],'avgscoreperlife':activity['values']['averageScorePerLife']['basic']['value'],'completed':activity['values']['completed']['basic']['displayValue'],'completionreason':activity['values']['completionReason']['basic']['displayValue'],'deaths':activity['values']['deaths']['basic']['value'],'efficiency':activity['values']['efficiency']['basic']['value'],'fireteamid':activity['values']['fireteamId']['basic']['displayValue'],'kills':activity['values']['kills']['basic']['value'],'killsdeathsassists':activity['values']['killsDeathsAssists']['basic']['value'],'killsdeathsratio':activity['values']['killsDeathsRatio']['basic']['value'],'opponentsdefeated':activity['values']['opponentsDefeated']['basic']['value'],'score':activity['values']['score']['basic']['value'],'standing':activity['values']['standing']['basic']['displayValue'],'team':activity['values']['team']['basic']['value'],'teamscore':activity['values']['teamScore']['basic']['value'],'timeplayed':activity['values']['timePlayedSeconds']['basic']['displayValue']}
					#print queryParams
					queryPath = 'destiny/activities/addActivity'
					system.db.runNamedQuery(queryPath, queryParams)
	except:
		logger.error("API Call Failed for Member ID " + str(destinyMembershipId) + " Character " + str(characterId))
		print "API Call Failed for Member ID " + str(destinyMembershipId) + " Character " + str(characterId)
			
def syncIronBanner():
	queryParams = {}
	#print queryParams
	queryPath = 'destiny/clans/getAllPlayers'
	playerList = system.dataset.toPyDataSet(system.db.runNamedQuery(queryPath, queryParams))
	for player in playerList:
		characters = json.loads(player['characterids'])
		for i in characters:
			ironBanner(player['membershiptype'],player['destinyid'],i)
