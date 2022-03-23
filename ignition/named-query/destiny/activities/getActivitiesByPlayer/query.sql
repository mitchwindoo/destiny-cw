WITH current_event AS (
		SELECT mode,start_date,end_date
		FROM events
		WHERE CURRENT_TIMESTAMP BETWEEN events.start_date AND events.end_date
), base_modifiers AS (
	SELECT 
	SUM(((activities.kills * 10) + (activities.assists * 2.5)) - (activities.deaths * 5)) AS score,
	activities.instanceid
	FROM activities
	INNER JOIN current_event ON activities.mode = current_event.mode
	WHERE TIMESTAMP BETWEEN current_event.start_date AND current_event.end_date 
	AND completed = 'Yes'
	AND activities.playerdestinyid = :destinyid 
	GROUP BY activities.instanceid
) SELECT
	*
FROM
	activities
	INNER JOIN players ON activities.playerdestinyid = players.destinyid
	INNER JOIN clans ON players.clanid = clans."id"
	INNER JOIN base_modifiers ON activities.instanceid = base_modifiers.instanceid
	INNER JOIN current_event ON activities.mode = current_event.mode
WHERE
	TIMESTAMP BETWEEN current_event.start_date AND current_event.end_date 
	AND completed = 'Yes'
	AND activities.playerdestinyid = :destinyid 
ORDER BY TIMESTAMP DESC