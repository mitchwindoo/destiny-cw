SELECT COUNT(*)
FROM players
WHERE
	destinyid = :playerid
	AND clanid = :clanid