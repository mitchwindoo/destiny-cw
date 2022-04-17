select * from events
WHERE end_date > CURRENT_TIMESTAMP
ORDER BY start_date asc