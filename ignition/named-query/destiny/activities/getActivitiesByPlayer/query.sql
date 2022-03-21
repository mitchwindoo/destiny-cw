WITH fireteam AS (
	SELECT COUNT
		( * ) * 1.05 AS clan_bonus,
		instanceid 
	FROM
		activities
		INNER JOIN players ON activities.playerdestinyid = players.destinyid 
	GROUP BY
		instanceid 
	HAVING
		COUNT ( * ) > 1 
	),
	calulations AS (
	SELECT
		ROUND( SUM ( ( activities.kills * activities.killsdeathsratio ) * 100 ) ) AS score,
		instanceid 
	FROM
		activities
		INNER JOIN players ON activities.playerdestinyid = players.destinyid 
	WHERE
		playerdestinyid = :destinyid
	GROUP BY
		instanceid 
	) SELECT
	* 
FROM
	activities
	INNER JOIN fireteam ON activities.instanceid = fireteam.instanceid
	INNER JOIN calulations ON activities.instanceid = calulations.instanceid
WHERE
	playerdestinyid = :destinyid
	AND TIMESTAMP BETWEEN '2022-03-15 17:00:00+00' 
	AND now( ) 
	AND completed = 'Yes' 
ORDER BY
TIMESTAMP DESC