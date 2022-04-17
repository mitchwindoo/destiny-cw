WITH events AS (SELECT id,mode,start_date,end_date FROM events WHERE events.id = :eventId)
SELECT
	AVG ( activities.killsdeathsratio ) AS "score",
	players."destinyid" AS "playerid" 
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
	AVG ( activities.killsdeathsratio ) DESC
LIMIT 1;