WITH current_event AS (
		SELECT mode,start_date,end_date
		FROM events
		WHERE CURRENT_TIMESTAMP BETWEEN events.start_date AND events.end_date
) SELECT
	MAX ((((activities.kills * 10) + (activities.assists * 2.5)) - (activities.deaths * 5))) AS "score",
	players."destinyid" AS "playerid"
FROM
	activities
	INNER JOIN players ON activities.playerdestinyid = players.destinyid
	INNER JOIN clans ON players.clanid = clans."id" 
	INNER JOIN current_event ON activities.mode = current_event.mode
WHERE
	clans."id" = :clanid 
	AND TIMESTAMP BETWEEN current_event.start_date AND current_event.end_date 
	AND completed = 'Yes'
GROUP BY
	players."destinyid"
ORDER BY
	score DESC
LIMIT 1