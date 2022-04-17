UPDATE
	sessions
SET
	theme = :new_theme
WHERE
	device_id = :device_id 