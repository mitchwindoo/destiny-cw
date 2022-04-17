--- Dynamic Activity Score
--- Get the Current Event Mode ID
WITH events AS (SELECT id,mode,start_date,end_date FROM events WHERE events.id = :eventId)
--- Main Query
SELECT
	activities.playerdestinyid as "playerid",
	ROUND(MAX({eventScoring})) AS "score"
FROM
	activities
	INNER JOIN events ON activities.mode = events.mode
	INNER JOIN players ON activities.playerdestinyid = players.destinyid
WHERE
	TIMESTAMP BETWEEN events.start_date AND events.end_date
	AND activities.mode = events.mode
	AND activities.completed = 'Yes'
	AND players.clanid = :clanId
GROUP BY
	playerid
ORDER BY
	score DESC
LIMIT 1