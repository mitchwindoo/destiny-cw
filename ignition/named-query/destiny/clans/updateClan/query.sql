UPDATE 
	clans
SET
	founder = :clanFounder,
	founderbungieid = :clanFounderBungieId,
	founderdestinyid = :clanFounderDestinyId,
	about = :clanAbout,
	registered_members = :clanMembers,
	motto = :clanMotto,
	callsign = :clanCallsign
WHERE 
	id = :clanId;