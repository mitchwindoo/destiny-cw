--- Dynamic Activity Score
--- Get the Current Event Mode ID
WITH events AS (SELECT id,mode,start_date,end_date FROM events WHERE events.id = :eventId)
--- Main Query
SELECT
	activities.playerdestinyid as "playerid",
	ROUND(AVG({eventScoring})) AS "score"
FROM
	activities
	INNER JOIN events ON activities.mode = events.mode
WHERE
	TIMESTAMP BETWEEN events.start_date AND events.end_date
	AND activities.mode = events.mode
	AND activities.completed = 'Yes'
	AND activities.playerdestinyid = :destinyid
GROUP BY
	activities.playerdestinyid
ORDER BY
	score DESC
LIMIT 1