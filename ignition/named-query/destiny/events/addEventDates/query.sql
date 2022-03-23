-- Run once to add the events into the database
INSERT INTO events(event_name,start_date,end_date)
VALUES (:eventName, :startDate, :endDate);