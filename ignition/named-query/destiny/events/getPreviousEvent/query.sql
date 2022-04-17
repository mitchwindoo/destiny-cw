SELECT * 
FROM events
WHERE CURRENT_TIMESTAMP - interval '12 hour' BETWEEN start_date AND end_date
LIMIT 1