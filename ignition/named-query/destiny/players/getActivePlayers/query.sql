SELECT
	*
FROM
	players
WHERE
	lastonline BETWEEN CURRENT_TIMESTAMP - INTERVAL '2 HOUR' AND CURRENT_TIMESTAMP
ORDER BY
	clanid