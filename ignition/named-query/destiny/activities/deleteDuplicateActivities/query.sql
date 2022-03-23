DELETE 
FROM
	activities 
WHERE
	id IN (
	SELECT id 
	FROM
		( SELECT id, ROW_NUMBER ( ) OVER ( PARTITION BY playerdestinyid, instanceid ORDER BY ID ) AS row_num FROM activities ) T 
	WHERE
	T.row_num > 1 
	);