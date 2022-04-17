--- Dynamic Activity Score
--- Get the Current Event Mode ID
WITH events AS (SELECT id,mode,start_date,end_date FROM events WHERE events.id = :eventId)
--- Main Query
SELECT
	players.clanid AS "clanId",
	ROUND(SUM({eventScoring})) AS game_score,
	ROW_NUMBER ( ) OVER ( ORDER BY ROUND(SUM({eventScoring})) DESC ) AS POSITION 
FROM
	activities
	INNER JOIN players ON activities.playerdestinyid = players.destinyid
	INNER JOIN clans ON players.clanid = clans."id"
	INNER JOIN events ON activities.mode = events.mode
WHERE
	TIMESTAMP BETWEEN events.start_date AND events.end_date
	AND activities.mode = events.mode
	AND activities.completed = 'Yes'
	{clanFilter}
GROUP BY
	"clanId",
	events.mode
ORDER BY
	game_score DESC
{LIMIT}