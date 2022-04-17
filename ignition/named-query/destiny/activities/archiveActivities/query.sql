DELETE FROM activities_archive;

INSERT INTO activities_testing
SELECT * FROM activities;

DELETE FROM activities;