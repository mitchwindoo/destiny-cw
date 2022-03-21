WITH avg AS (SELECT script_runtime from script_logs where script = :script ORDER BY script_timestamp desc limit 5
)
SELECT AVG
	( script_runtime ) from avg