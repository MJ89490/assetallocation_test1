/* ---------------------------------------------------- */
/*  Generated by Enterprise Architect Version 12.0 		*/
/*  Created On : 06-Aug-2020 10:13:39 				*/
/*  DBMS       : PostgreSQL 						*/
/* ---------------------------------------------------- */

/* Drop Sequences for Autonumber Columns */

DROP SEQUENCE IF EXISTS "arp"."fica_asset_id_seq" CASCADE
;

/* Drop Tables */

DROP TABLE IF EXISTS "arp"."fica_asset" CASCADE
;

/* Create Tables */

CREATE TABLE "arp"."fica_asset"
(
	"asset_id" integer NOT NULL,
	"id" serial NOT NULL,
	"fica_asset_group_id" integer NOT NULL,
	"category" varchar(50)	 NOT NULL,
	"curve_tenor" varchar(5)	 NULL,
	"execution_state_id" integer NOT NULL
)
;
/* Create Primary Keys, Indexes, Uniques, Checks */

ALTER TABLE "arp"."fica_asset" ADD CONSTRAINT "fica_asset_pkey"
	PRIMARY KEY ("id")
;

ALTER TABLE "arp"."fica_asset" ADD CONSTRAINT "category_check" CHECK (category IN ('future', 'sovereign', 'swap', 'swap_cr'))
;

ALTER TABLE "arp"."fica_asset" ADD CONSTRAINT "curve_tenor_check" CHECK (curve_tenor IN ('mth3', 'yr1', 'yr2', 'yr3', 'yr4', 'yr5', 'yr6', 'yr7', 'yr8', 'yr9', 'yr10', 'yr15', 'yr20', 'yr30'))
;
/* Create Foreign Key Constraints */

ALTER TABLE "arp"."fica_asset" ADD CONSTRAINT "fica_asset_asset_fkey"
	FOREIGN KEY ("asset_id") REFERENCES "asset"."asset" ("id") ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE "arp"."fica_asset" ADD CONSTRAINT "fica_asset_execution_state_fkey"
	FOREIGN KEY ("execution_state_id") REFERENCES "config"."execution_state" ("id") ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE "arp"."fica_asset" ADD CONSTRAINT "fica_asset_fica_asset_group_fkey"
	FOREIGN KEY ("fica_asset_group_id") REFERENCES "arp"."fica_asset_group" ("id") ON DELETE No Action ON UPDATE No Action
;
