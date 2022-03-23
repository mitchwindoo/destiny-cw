SELECT
	script_timestamp 
FROM
	script_logs 
GROUP BY
	script,
	script_timestamp 
ORDER BY
	script_timestamp DESC 
	LIMIT 1