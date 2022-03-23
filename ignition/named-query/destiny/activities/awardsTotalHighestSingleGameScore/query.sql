WITH current_event AS (
		SELECT mode,start_date,end_date
		FROM events
		WHERE CURRENT_TIMESTAMP BETWEEN events.start_date AND events.end_date
), clan_bonus AS (
	SELECT
	count (*) * 1.05 as value,
	instanceid
FROM
	activities
	INNER JOIN players ON activities.playerdestinyid = players.destinyid
GROUP BY instanceid
)SELECT
	MAX ((((activities.kills * 10) + (activities.assists * 2.5)) - (activities.deaths * 5)) * clan_bonus.value) AS "score",
	players."destinyid" AS "playerid"
FROM
	activities
	INNER JOIN players ON activities.playerdestinyid = players.destinyid
	INNER JOIN clans ON players.clanid = clans."id" 
	INNER JOIN current_event ON activities.mode = current_event.mode
	INNER JOIN clan_bonus ON activities.instanceid = clan_bonus.instanceid
WHERE
	TIMESTAMP BETWEEN current_event.start_date AND current_event.end_date 
	AND completed = 'Yes'
GROUP BY
	players."destinyid"
HAVING COUNT (activities.playerdestinyid) > 10
ORDER BY
	score DESC
LIMIT 1


