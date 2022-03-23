-- Regular Update to the dates
UPDATE events
SET start_date = :startDate, end_date = :endDate
WHERE event_name = :eventName;