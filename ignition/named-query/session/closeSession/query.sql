UPDATE sessions
SET end_time = CURRENT_TIMESTAMP
WHERE id = :id