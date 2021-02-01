/* ---------------------------------------------------- */
/*  Generated by Enterprise Architect Version 12.0 		*/
/*  Created On : 06-Aug-2020 10:13:39 				*/
/*  DBMS       : PostgreSQL 						*/
/* ---------------------------------------------------- */

/* Drop Sequences for Autonumber Columns */

DROP SEQUENCE IF EXISTS "arp"."strategy_asset_analytic_id_seq" CASCADE
;

/* Drop Tables */

DROP TABLE IF EXISTS "arp"."strategy_asset_analytic" CASCADE
;

/* Create Tables */

CREATE TABLE "arp"."strategy_asset_analytic"
(
	"id" serial NOT NULL,
	"strategy_id" integer NOT NULL,
	"asset_id" integer NOT NULL,
	"business_date" date NOT NULL,
	"category" varchar(50)	 NOT NULL,
	"subcategory" varchar(50)	 NOT NULL,
	"frequency" arp.frequency NOT NULL,
	"value" numeric(32,16) NOT NULL,
	"execution_state_id" integer NOT NULL
)
;
/* Create Primary Keys, Indexes, Uniques, Checks */

ALTER TABLE "arp"."strategy_asset_analytic" ADD CONSTRAINT "strategy_asset_analytic_pkey"
	PRIMARY KEY ("id")
;

ALTER TABLE
	"arp"."strategy_asset_analytic"
ADD CONSTRAINT
	"strategy_asset_analytic_strategy_id_asset_id_business_date_category_subcategory_key"
UNIQUE
	("strategy_id","asset_id","business_date", "category","subcategory")
;

/* Create Foreign Key Constraints */

ALTER TABLE "arp"."strategy_asset_analytic" ADD CONSTRAINT "strategy_asset_analytic_execution_state_fkey"
	FOREIGN KEY ("execution_state_id") REFERENCES "config"."execution_state" ("id") ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE "arp"."strategy_asset_analytic" ADD CONSTRAINT "strategy_asset_analytic_asset_fkey"
	FOREIGN KEY ("asset_id") REFERENCES "asset"."asset" ("id") ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE "arp"."strategy_asset_analytic" ADD CONSTRAINT "strategy_asset_analytic_strategy_fkey"
	FOREIGN KEY ("strategy_id") REFERENCES "arp"."strategy" ("id") ON DELETE No Action ON UPDATE No Action
;