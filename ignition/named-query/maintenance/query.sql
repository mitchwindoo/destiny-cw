DELETE FROM script_logs
WHERE script_timestamp < now() - interval '1 week';
DELETE FROM sessions
WHERE start_time < now() - interval '1 week';