WITH current_event AS (SELECT mode,start_date,end_date FROM events WHERE CURRENT_TIMESTAMP BETWEEN events.start_date AND events.end_date)
SELECT
	COUNT(DISTINCT(activities.playerdestinyid))
FROM
	activities
	INNER JOIN players ON activities.playerdestinyid = players.destinyid
	INNER JOIN clans ON players.clanid = clans."id"
	INNER JOIN current_event ON activities.mode = current_event.mode
WHERE clans.id = :clanId
AND TIMESTAMP BETWEEN current_event.start_date AND current_event.end_date 
AND activities.mode = current_event.mode