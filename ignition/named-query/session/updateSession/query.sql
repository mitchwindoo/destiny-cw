UPDATE 
	sessions 
SET
	id = :id,
	start_time = CURRENT_TIMESTAMP,
	device_ip = :host,
	timezone = :timezone,
	device_useragent = :useragent,
	session_type = 'returning'
WHERE
	device_id = :device_id