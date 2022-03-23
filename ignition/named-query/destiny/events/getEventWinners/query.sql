SELECT
	event_history.event_name as "Event", 
	event_history.end_date as "Completion Date", 
	(SELECT name from clans where id = event_history.overall_winner_clanid) as "Overall", 
	event_history.overall_winner_score as "Overall Score", 
	(SELECT name from clans where id = event_history.lclan_winner_clanid) as "Large Clan", 
	event_history.lclan_winner_score as "Large Clan Score",
	(SELECT name from clans where id = event_history.mclan_winner_clanid) as "Medium Clan", 
	event_history.mclan_winner_score as "Medium Clan Score", 
	(SELECT name from clans where id = event_history.sclan_winner_clanid) as "Small Clan", 
	event_history.sclan_winner_score as "Small Clan Score"
FROM
	event_history
ORDER BY
	end_date DESC