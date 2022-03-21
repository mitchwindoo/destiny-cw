SELECT
	script_timestamp 
FROM
	script_logs 
WHERE
	script = :script
GROUP BY
	script,
	script_timestamp 
ORDER BY
	script_timestamp DESC 
	LIMIT 1