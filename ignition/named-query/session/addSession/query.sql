INSERT INTO sessions (id,start_time,device_ip,timezone,device_useragent,device_id)
VALUES (:id, CURRENT_TIMESTAMP, :host, :timezone, :useragent, :device_id)