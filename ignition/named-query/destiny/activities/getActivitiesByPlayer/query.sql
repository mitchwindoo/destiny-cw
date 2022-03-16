SELECT *
FROM activities
WHERE playerdestinyid = :destinyid AND timestamp between '2022-03-15 17:00:00+00' and now()
ORDER BY timestamp desc