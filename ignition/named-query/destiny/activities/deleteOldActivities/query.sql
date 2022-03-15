DELETE FROM activities
WHERE timestamp < now() - interval '3 month';