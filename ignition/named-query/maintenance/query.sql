-- Delete old script logs
DELETE FROM script_logs
WHERE script_timestamp < now() - interval '1 week';
-- Delete old session information
DELETE FROM sessions
WHERE start_time < now() - interval '1 week';
-- Delete players if their clan doesn't exist anymore
DELETE FROM players WHERE clanid NOT IN (SELECT clans.id FROM clans);