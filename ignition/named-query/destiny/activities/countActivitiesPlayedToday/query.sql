SELECT count(*)
from activities
where timestamp > now() - interval '24 hour'