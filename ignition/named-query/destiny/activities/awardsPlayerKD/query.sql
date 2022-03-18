SELECT
	AVG ( activities.killsdeathsratio ) AS "score",
	players."destinyid" AS "playerid" 
FROM
	activities
	INNER JOIN players ON activities.playerdestinyid = players.destinyid
	INNER JOIN clans ON players.clanid = clans."id" 
WHERE
	players."destinyid" = :playerid
	AND TIMESTAMP BETWEEN '2022-03-15 17:00:00+00' 
	AND now( ) 
GROUP BY
	players."destinyid"
HAVING COUNT (activities.playerdestinyid) > 10
ORDER BY
	AVG ( activities.killsdeathsratio ) DESC
LIMIT 1;