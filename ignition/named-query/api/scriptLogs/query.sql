INSERT INTO script_logs (script,script_runtime,script_timestamp)
VALUES (:script, :script_runtime, CURRENT_TIMESTAMP)