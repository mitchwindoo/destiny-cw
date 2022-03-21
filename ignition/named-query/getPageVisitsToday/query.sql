select count (distinct(device_ip))
from sessions
where start_time > now() - interval '24 hour'