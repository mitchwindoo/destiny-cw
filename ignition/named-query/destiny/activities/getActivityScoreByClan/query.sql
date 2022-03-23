WITH current_event AS (
	SELECT mode,start_date,end_date
	FROM events
	WHERE CURRENT_TIMESTAMP BETWEEN events.start_date AND events.end_date
)SELECT
	players."destinyid" AS "playerid", 
	ROUND ( SUM((((activities.kills * 10) + (activities.assists * 2.5)) - (activities.deaths * 5)))) as game_score,
	ROW_NUMBER ( ) OVER ( ORDER BY SUM((((activities.kills * 10) + (activities.assists * 2.5)) - (activities.deaths * 5))) DESC ) AS POSITION,
	COUNT (activities.playerdestinyid) as "gamesplayed"
FROM
	activities
	INNER JOIN players ON activities.playerdestinyid = players.destinyid
	INNER JOIN clans ON players.clanid = clans."id"
	INNER JOIN current_event ON activities.mode = current_event.mode
WHERE
	TIMESTAMP BETWEEN current_event.start_date AND current_event.end_date 
	AND completed = 'Yes'
	AND clans."id" = :clanid 
GROUP BY
	players."destinyid"
ORDER BY
	game_score DESC