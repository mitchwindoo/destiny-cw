SELECT
	ROUND(SUM((activities.kills * activities.killsdeathsratio) * 100)) AS "score", 
	players."name" AS "playerName", 
	clans."name" AS "clanName",
	ROW_NUMBER () OVER (ORDER BY SUM((activities.kills * activities.killsdeathsratio) * 100) desc) as position
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
	players."name",
	clans."name"
ORDER BY
	SUM((activities.kills * activities.killsdeathsratio) * 100) desc