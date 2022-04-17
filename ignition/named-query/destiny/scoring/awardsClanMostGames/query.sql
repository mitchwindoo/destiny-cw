WITH events AS (SELECT id,mode,start_date,end_date FROM events WHERE events.id = :eventId)
SELECT
	players."destinyid" as "playerid",
	COUNT (activities.playerdestinyid) as "score"
FROM
	activities
	INNER JOIN players ON activities.playerdestinyid = players.destinyid
	INNER JOIN clans ON players.clanid = clans."id"
	INNER JOIN events ON activities.mode = events.mode
WHERE 
	clans."id" = :clanid
	AND TIMESTAMP BETWEEN events.start_date AND events.end_date 
	AND completed = 'Yes'
GROUP BY
	players."destinyid"
ORDER BY
	COUNT (players."destinyid") desc
