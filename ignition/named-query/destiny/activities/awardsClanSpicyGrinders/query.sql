SELECT
	COUNT(players.destinyid) AS score, 
	players."name"
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
	clans."id" = :clanid AND
	"timestamp" BETWEEN '2022-03-15 17:00:00+00' AND now( )
GROUP BY
	players.destinyid
HAVING
	COUNT(activities.playerdestinyid) > 50
ORDER BY
	COUNT(players.destinyid) DESC;