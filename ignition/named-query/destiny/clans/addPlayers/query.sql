INSERT INTO players(destinyid,name,clanid,membershiptype,characterids)
VALUES (:destinyid,:name,:clanid,:membershiptype,:characterids::jsonb)