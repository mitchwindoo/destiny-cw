SELECT * 
FROM events
WHERE CURRENT_TIMESTAMP BETWEEN start_date AND end_date
LIMIT 1