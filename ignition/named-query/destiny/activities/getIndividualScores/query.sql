SELECT
	ROUND(SUM((activities.kills * activities.killsdeathsratio) * 100)) AS "score", 
	players."destinyid" AS "playerid", 
	clans."id" AS "clanid",
	ROW_NUMBER () OVER (ORDER BY SUM((activities.kills * activities.killsdeathsratio) * 100) desc) as position,
	COUNT (players."destinyid") as "gamesplayed"
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
WHERE timestamp between '2022-03-15 17:00:00+00' and now()
GROUP BY
	players."destinyid",
	clans."id"
ORDER BY
	SUM((activities.kills * activities.killsdeathsratio) * 100) desc