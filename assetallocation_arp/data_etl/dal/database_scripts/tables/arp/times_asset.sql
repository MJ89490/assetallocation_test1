/* ---------------------------------------------------- */
/*  Generated by Enterprise Architect Version 12.0 		*/
/*  Created On : 06-Aug-2020 10:13:39 				*/
/*  DBMS       : PostgreSQL 						*/
/* ---------------------------------------------------- */

/* Drop Sequences for Autonumber Columns */

DROP SEQUENCE IF EXISTS "arp"."times_asset_id_seq" CASCADE
;

/* Drop Tables */

DROP TABLE IF EXISTS "arp"."times_asset" CASCADE
;

/* Create Tables */

CREATE TABLE "arp"."times_asset"
(
	"id" serial NOT NULL,
	"signal_asset_id" integer NOT NULL,
	"future_asset_id" integer NOT NULL,
	"asset_subcategory" varchar(25) NOT NULL,
	"s_leverage" integer NULL,
	"strategy_id" integer NOT NULL,
	"cost" numeric(32,16) NULL,
	"execution_state_id" integer NOT NULL
)
;

/* Create Primary Keys, Indexes, Uniques, Checks */

ALTER TABLE "arp"."times_asset" ADD CONSTRAINT "times_asset_pkey"
	PRIMARY KEY ("id")
;

ALTER TABLE "arp"."times_asset" ADD CONSTRAINT "times_asset_strategy_id_asset_subcategory_key"
	UNIQUE ("strategy_id", "asset_subcategory")
;

/* Create Foreign Key Constraints */

ALTER TABLE "arp"."times_asset" ADD CONSTRAINT "times_asset_asset_signal_fkey"
	FOREIGN KEY ("signal_asset_id") REFERENCES "asset"."asset" ("id") ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE "arp"."times_asset" ADD CONSTRAINT "times_asset_asset_future_fkey"
	FOREIGN KEY ("future_asset_id") REFERENCES "asset"."asset" ("id") ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE "arp"."times_asset" ADD CONSTRAINT "times_asset_execution_state_fkey"
	FOREIGN KEY ("execution_state_id") REFERENCES "config"."execution_state" ("id") ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE "arp"."times_asset" ADD CONSTRAINT "times_asset_times_fkey"
	FOREIGN KEY ("strategy_id") REFERENCES "arp"."times" ("strategy_id") ON DELETE No Action ON UPDATE No Action
;