DELETE FROM activities_archive;

INSERT INTO activities_archive
SELECT * FROM activities;

DELETE FROM activities;