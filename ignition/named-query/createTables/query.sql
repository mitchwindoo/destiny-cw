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

 Date: 15/03/2022 10:19:49
*/


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
  "avgscoreperkill" float4 NOT NULL,
  "avgscoreperlife" float4 NOT NULL,
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
  "playercharacterid" int8 NOT NULL
)
;
ALTER TABLE "public"."activities" OWNER TO "postgres";

-- ----------------------------
-- Table structure for activities_archive
-- ----------------------------
DROP TABLE IF EXISTS "public"."activities_archive";
CREATE TABLE "public"."activities_archive" (
  "playerdestinyid" int8 NOT NULL,
  "instanceid" int8 NOT NULL,
  "modes" jsonb NOT NULL,
  "mode" int2 NOT NULL,
  "isprivate" bool NOT NULL,
  "referenceid" int8 NOT NULL,
  "timestamp" timestamptz(6) NOT NULL,
  "activityduration" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "assists" int4 NOT NULL,
  "avgscoreperkill" float4 NOT NULL,
  "avgscoreperlife" float4 NOT NULL,
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
  "playercharacterid" int8 NOT NULL
)
;
ALTER TABLE "public"."activities_archive" OWNER TO "postgres";

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
  "motto" varchar(255) COLLATE "pg_catalog"."default" NOT NULL
)
;
ALTER TABLE "public"."clans" OWNER TO "postgres";

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
