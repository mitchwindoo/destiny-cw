DELETE 
FROM
	activities 
WHERE
	ID IN (
	SELECT ID 
	FROM
		( SELECT ID, ROW_NUMBER ( ) OVER ( PARTITION BY playerdestinyid, instanceid ORDER BY ID ) AS row_num FROM activities ) T 
	WHERE
	T.row_num > 1 
	);