SELECT
	players."destinyid" as "playerid",
	COUNT (activities.playerdestinyid) as "score"
FROM
	activities
	INNER JOIN
	players
	ON 
		activities.playerdestinyid = players.destinyid
	INNER JOIN
	clans
	ON 
		players.clanid = clans."id"
WHERE 
	timestamp between '2022-03-15 17:00:00+00' and now()
GROUP BY
	players."destinyid"
ORDER BY
	COUNT (players."destinyid") desc
LIMIT 1