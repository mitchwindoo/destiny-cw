WITH current_event AS (
		SELECT mode,start_date,end_date
		FROM events
		WHERE CURRENT_TIMESTAMP BETWEEN events.start_date AND events.end_date
)SELECT
	AVG ( activities.killsdeathsratio ) AS "score",
	players."destinyid" AS "playerid" 
FROM
	activities
	INNER JOIN players ON activities.playerdestinyid = players.destinyid
	INNER JOIN clans ON players.clanid = clans."id" 
	INNER JOIN current_event ON activities.mode = current_event.mode
WHERE
	TIMESTAMP BETWEEN current_event.start_date AND current_event.end_date 
	AND completed = 'Yes'
GROUP BY
	players."destinyid"
HAVING COUNT (activities.playerdestinyid) > 10
ORDER BY
	AVG ( activities.killsdeathsratio ) DESC
LIMIT 1;