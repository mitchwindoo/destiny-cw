--- Dynamic Activity Score
--- Get the Current Event Mode ID
WITH events AS (SELECT id,mode,start_date,end_date FROM events WHERE events.id = :eventId),
calcs AS (
SELECT 
	activities.instanceid,
	ROUND(SUM({eventScoring})) AS game_score
FROM
	activities
	INNER JOIN events ON activities.mode = events.mode
WHERE
	TIMESTAMP BETWEEN events.start_date AND events.end_date 
	AND activities.mode = events.mode
	AND activities.completed = 'Yes'
	AND activities.playerdestinyid = :destinyId
GROUP BY 
	activities.instanceid) 
--- Main Query
SELECT
	activities.playerdestinyid,
	activities.playercharacterid,
	activities.instanceid,
	activities.mode,
	activities.timestamp,
	activities.killsdeathsratio,
	activities.kills,
	activities.deaths,
	activities.assists,
	activities.efficiency,
	activities.score,
	activities.standing,
	calcs.game_score
FROM
	activities
	INNER JOIN events ON activities.mode = events.mode
	INNER JOIN calcs ON calcs.instanceid = activities.instanceid
WHERE
	TIMESTAMP BETWEEN events.start_date AND events.end_date
	AND activities.mode = events.mode
	AND activities.completed = 'Yes'
	AND activities.playerdestinyid = :destinyId
ORDER BY
	timestamp DESC
{LIMIT}