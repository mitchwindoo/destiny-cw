/*
 Navicat PostgreSQL Data Transfer

 Source Server         : Destiny-CW
 Source Server Type    : PostgreSQL
 Source Server Version : 120009
 Source Host           : localhost:5432
 Source Catalog        : destiny-cw
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 120009
 File Encoding         : 65001

 Date: 23/03/2022 16:00:24
*/


-- ----------------------------
-- Sequence structure for activities_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."activities_id_seq";
CREATE SEQUENCE "public"."activities_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;
ALTER SEQUENCE "public"."activities_id_seq" OWNER TO "postgres";

-- ----------------------------
-- Table structure for activities
-- ----------------------------
DROP TABLE IF EXISTS "public"."activities";
CREATE TABLE "public"."activities" (
  "playerdestinyid" int8 NOT NULL,
  "instanceid" int8 NOT NULL,
  "modes" jsonb NOT NULL,
  "mode" int2 NOT NULL,
  "isprivate" bool NOT NULL,
  "referenceid" int8 NOT NULL,
  "timestamp" timestamptz(6) NOT NULL,
  "activityduration" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "assists" int4 NOT NULL,
  "completed" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "completionreason" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "deaths" float4 NOT NULL,
  "efficiency" float4 NOT NULL,
  "fireteamid" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "kills" int4 NOT NULL,
  "killsdeathsassists" float4 NOT NULL,
  "killsdeathsratio" float4 NOT NULL,
  "opponentsdefeated" int4 NOT NULL,
  "score" int4 NOT NULL,
  "standing" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "team" int4 NOT NULL,
  "teamscore" int4 NOT NULL,
  "timeplayed" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "playercharacterid" int8 NOT NULL,
  "pgcr_extended" json NOT NULL,
  "id" int4 NOT NULL DEFAULT nextval('activities_id_seq'::regclass)
)
;
ALTER TABLE "public"."activities" OWNER TO "postgres";

-- ----------------------------
-- Table structure for api_keys
-- ----------------------------
DROP TABLE IF EXISTS "public"."api_keys";
CREATE TABLE "public"."api_keys" (
  "key" varchar(255) COLLATE "pg_catalog"."default" NOT NULL
)
;
ALTER TABLE "public"."api_keys" OWNER TO "postgres";

-- ----------------------------
-- Table structure for clans
-- ----------------------------
DROP TABLE IF EXISTS "public"."clans";
CREATE TABLE "public"."clans" (
  "id" int8 NOT NULL,
  "name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "founder" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "founderbungieid" int8 NOT NULL,
  "founderdestinyid" int8 NOT NULL,
  "about" text COLLATE "pg_catalog"."default" NOT NULL,
  "members" int8 NOT NULL,
  "motto" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "callsign" varchar(255) COLLATE "pg_catalog"."default" NOT NULL
)
;
ALTER TABLE "public"."clans" OWNER TO "postgres";

-- ----------------------------
-- Table structure for event_history
-- ----------------------------
DROP TABLE IF EXISTS "public"."event_history";
CREATE TABLE "public"."event_history" (
  "event_name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "end_date" date NOT NULL,
  "overall_winner_clanid" int8 NOT NULL,
  "overall_winner_score" float8 NOT NULL,
  "sclan_winner_clanid" int8 NOT NULL,
  "sclan_winner_score" float8 NOT NULL,
  "mclan_winner_clanid" int8 NOT NULL,
  "mclan_winner_score" float8 NOT NULL,
  "lclan_winner_clanid" int8 NOT NULL,
  "lclan_winner_score" float8 NOT NULL
)
;
ALTER TABLE "public"."event_history" OWNER TO "postgres";

-- ----------------------------
-- Table structure for events
-- ----------------------------
DROP TABLE IF EXISTS "public"."events";
CREATE TABLE "public"."events" (
  "event_name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "start_date" timestamptz(6) NOT NULL,
  "end_date" timestamptz(6) NOT NULL,
  "mode" int2
)
;
ALTER TABLE "public"."events" OWNER TO "postgres";

-- ----------------------------
-- Table structure for players
-- ----------------------------
DROP TABLE IF EXISTS "public"."players";
CREATE TABLE "public"."players" (
  "destinyid" int8 NOT NULL,
  "name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "clanid" int8 NOT NULL,
  "membershiptype" int2 NOT NULL,
  "characterids" jsonb NOT NULL
)
;
ALTER TABLE "public"."players" OWNER TO "postgres";

-- ----------------------------
-- Table structure for script_logs
-- ----------------------------
DROP TABLE IF EXISTS "public"."script_logs";
CREATE TABLE "public"."script_logs" (
  "script" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "script_runtime" float4 NOT NULL,
  "script_timestamp" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;
ALTER TABLE "public"."script_logs" OWNER TO "postgres";

-- ----------------------------
-- Table structure for sessions
-- ----------------------------
DROP TABLE IF EXISTS "public"."sessions";
CREATE TABLE "public"."sessions" (
  "id" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "start_time" timestamptz(6) NOT NULL,
  "end_time" timestamptz(6),
  "device_ip" varchar(255) COLLATE "pg_catalog"."default",
  "timezone" varchar(255) COLLATE "pg_catalog"."default",
  "device_useragent" text COLLATE "pg_catalog"."default",
  "device_id" varchar(255) COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."sessions" OWNER TO "postgres";

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."activities_id_seq"
OWNED BY "public"."activities"."id";
SELECT setval('"public"."activities_id_seq"', 6616, true);

-- ----------------------------
-- Primary Key structure for table activities
-- ----------------------------
ALTER TABLE "public"."activities" ADD CONSTRAINT "activities_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table api_keys
-- ----------------------------
ALTER TABLE "public"."api_keys" ADD CONSTRAINT "api_keys_pkey" PRIMARY KEY ("key");

-- ----------------------------
-- Primary Key structure for table clans
-- ----------------------------
ALTER TABLE "public"."clans" ADD CONSTRAINT "clans_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table players
-- ----------------------------
ALTER TABLE "public"."players" ADD CONSTRAINT "players_pkey" PRIMARY KEY ("destinyid");
