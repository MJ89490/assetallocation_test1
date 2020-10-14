/* ---------------------------------------------------- */
/*  Generated by Enterprise Architect Version 12.0 		*/
/*  Created On : 06-Aug-2020 10:13:39 				*/
/*  DBMS       : PostgreSQL 						*/
/* ---------------------------------------------------- */

/* Drop Sequences for Autonumber Columns */

DROP SEQUENCE IF EXISTS "arp"."fica_version_seq" CASCADE
;

/* Drop Tables */

DROP TABLE IF EXISTS "arp"."fica" CASCADE
;

/* Create Tables */

CREATE TABLE "arp"."fica"
(
	"tenor" integer NOT NULL,
	"coupon" numeric(32,16) NOT NULL,
	"curve" varchar(50)	 NOT NULL,
	"trading_cost" integer NOT NULL,
	"business_tstzrange" tstzrange NOT NULL,
	"strategy_weights" numeric(32,16) [] NOT NULL,
	"strategy_id" integer NOT NULL,
	"execution_state_id" integer NOT NULL,
	"version" serial NOT NULL
)
;
/* Create Primary Keys, Indexes, Uniques, Checks */

ALTER TABLE "arp"."fica" ADD CONSTRAINT "fica_pkey"
	PRIMARY KEY ("strategy_id")
;

/* Create Foreign Key Constraints */

ALTER TABLE "arp"."fica" ADD CONSTRAINT "fica_execution_state_fkey"
	FOREIGN KEY ("execution_state_id") REFERENCES "config"."execution_state" ("id") ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE "arp"."fica" ADD CONSTRAINT "fica_strategy_fkey"
	FOREIGN KEY ("strategy_id") REFERENCES "arp"."strategy" ("id") ON DELETE No Action ON UPDATE No Action
;