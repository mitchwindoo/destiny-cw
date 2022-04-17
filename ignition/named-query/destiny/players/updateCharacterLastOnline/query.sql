UPDATE players
SET characterids = :characterInfo::jsonb
WHERE destinyid = :playerid::bigint;