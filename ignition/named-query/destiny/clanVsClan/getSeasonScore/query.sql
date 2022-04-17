SELECT
	players.clanid AS "clanId",
	ROUND(SUM((((activities.kills*10)+(activities.assists*2.5)+ (CASE WHEN activities.standing = 'Victory' THEN 100 ELSE 0 END))-(activities.deaths*5)*activities.clan_bonus))) AS game_score,
	ROW_NUMBER ( ) OVER ( ORDER BY ROUND(SUM((((activities.kills*10)+(activities.assists*2.5))-(activities.deaths*5)*activities.clan_bonus))) DESC ) AS POSITION 
FROM
	activities
	INNER JOIN players ON activities.playerdestinyid = players.destinyid
	INNER JOIN clans ON players.clanid = clans."id"
WHERE
	TIMESTAMP BETWEEN '2022-02-22 17:00:00+00' AND '2022-05-24 17:00:00+00'
	AND activities.mode = 32
	AND activities.completed = 'Yes'
GROUP BY
	"clanId"
ORDER BY
	game_score DESC