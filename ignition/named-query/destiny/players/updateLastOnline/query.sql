UPDATE players
SET lastonline = :lastonline
WHERE destinyid = :playerid::bigint;