/* ---------------------------------------------------- */
/*  Generated by Enterprise Architect Version 12.0 		*/
/*  Created On : 06-Aug-2020 10:13:39 				*/
/*  DBMS       : PostgreSQL 						*/
/* ---------------------------------------------------- */

/* Drop Sequences for Autonumber Columns */

DROP SEQUENCE IF EXISTS "arp"."strategy_asset_id_seq" CASCADE
;

/* Drop Tables */

DROP TABLE IF EXISTS "arp"."strategy_asset" CASCADE
;

/* Create Tables */

CREATE TABLE "arp"."strategy_asset"
(
	"id" serial NOT NULL,
	"strategy_asset_group_id" INTEGER NOT NULL,
	"asset_id" integer NOT NULL,
	"name" varchar(50) NOT NULL,
	"execution_state_id" integer NOT NULL
)
;

/* Create Primary Keys, Indexes, Uniques, Checks */

ALTER TABLE "arp"."strategy_asset" ADD CONSTRAINT "strategy_asset_pkey"
	PRIMARY KEY ("id")
;

ALTER TABLE "arp"."strategy_asset" ADD CONSTRAINT "strategy_asset_group_id_name_key" UNIQUE ("strategy_asset_group_id", "name")
;

/* Create Foreign Key Constraints */

ALTER TABLE "arp"."strategy_asset" ADD CONSTRAINT "strategy_asset_asset_fkey"
	FOREIGN KEY ("asset_id") REFERENCES "asset"."asset" ("id") ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE "arp"."strategy_asset" ADD CONSTRAINT "strategy_asset_strategy_asset_group_fkey"
	FOREIGN KEY ("strategy_asset_group_id") REFERENCES "arp"."strategy_asset_group" ("id") ON DELETE CASCADE ON UPDATE No Action
;

ALTER TABLE "arp"."strategy_asset" ADD CONSTRAINT "strategy_asset_execution_state_fkey"
	FOREIGN KEY ("execution_state_id") REFERENCES "config"."execution_state" ("id") ON DELETE No Action ON UPDATE No Action
;