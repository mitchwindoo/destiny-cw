-- getActivityScoreByClan
-- Get the Current Event Mode ID
WITH current_event AS (
		SELECT mode,start_date,end_date
		FROM events
		WHERE id = :eventid
),
--- Calculate the score for each event mode
calcs AS (
SELECT 
	players.destinyid AS "playerid",
	CASE
		WHEN current_event.mode = 19 -- Iron Banner
			THEN ROUND(SUM((((activities.kills*10)+(activities.assists*2.5))-(activities.deaths*5))))
		WHEN current_event.mode = 84 -- Trials of Osiris
			THEN ROUND(SUM((((activities.kills*10)+(activities.assists*2.5))-(activities.deaths*5))))
		WHEN current_event.mode = 46 -- Nightfalls
			THEN ROUND(SUM(activities.score))
		WHEN current_event.mode = 4 -- Raids
			THEN ROUND(SUM(((activities.kills*10) + (activities.completed_value*5000)) - (activities.deaths*50) * activities.clan_bonus))
		WHEN current_event.mode = 82 -- Dungeons
			THEN ROUND(SUM(activities.score))
	END AS game_score
FROM
	activities
	INNER JOIN players ON activities.playerdestinyid = players.destinyid
	INNER JOIN clans ON players.clanid = clans."id"
	INNER JOIN current_event ON activities.mode = current_event.mode
WHERE
	TIMESTAMP BETWEEN current_event.start_date AND current_event.end_date 
	AND completed = 'Yes'
	AND activities.mode = current_event.mode
	AND clans."id" = :clanid
GROUP BY
	players.destinyid,
	current_event.mode) 
--- Main Query
SELECT
	clans."id" AS "clanid",
	players.destinyid AS "playerid",
	calcs.game_score AS game_score,
	ROW_NUMBER ( ) OVER ( ORDER BY calcs.game_score DESC ) AS POSITION,
	COUNT (players."destinyid") as "gamesplayed"
FROM
	activities
	INNER JOIN players ON activities.playerdestinyid = players.destinyid
	INNER JOIN clans ON players.clanid = clans."id"
	INNER JOIN current_event ON activities.mode = current_event.mode
	INNER JOIN calcs ON calcs.playerid = activities.playerdestinyid
WHERE
	TIMESTAMP BETWEEN current_event.start_date AND current_event.end_date 
	AND completed = 'Yes'
	AND activities.mode = current_event.mode
	AND clans."id" = :clanid
	AND game_score IS NOT NULL
GROUP BY
	players.destinyid,
	clans."id",
	current_event.mode,
	calcs.game_score
ORDER BY
	game_score DESC