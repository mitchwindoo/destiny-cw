INSERT INTO activities(playercharacterid,playerdestinyid,instanceid,modes,mode,isprivate,referenceid,timestamp,activityduration,assists,avgscoreperkill,avgscoreperlife,completed,completionreason,deaths,efficiency,fireteamid,kills,killsdeathsassists,killsdeathsratio,opponentsdefeated,score,standing,team,teamscore,timeplayed,pgcr_extended)
VALUES (:playercharacterid,:playerdestinyid,:instanceid,:modes::jsonb,:mode,:isprivate,:referenceid,:timestamp,:activityduration,:assists,:avgscoreperkill,:avgscoreperlife,:completed,:completionreason,:deaths,:efficiency,:fireteamid,:kills,:killsdeathsassists,:killsdeathsratio,:opponentsdefeated,:score,:standing,:team,:teamscore,:timeplayed, :pgcr_extended::json)