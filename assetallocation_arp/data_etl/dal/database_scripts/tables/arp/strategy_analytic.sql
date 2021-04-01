/* ---------------------------------------------------- */
/*  Generated by Enterprise Architect Version 12.0 		*/
/*  Created On : 06-Aug-2020 10:13:39 				*/
/*  DBMS       : PostgreSQL 						*/
/* ---------------------------------------------------- */

/* Drop Sequences for Autonumber Columns */

DROP SEQUENCE IF EXISTS "arp"."strategy_analytic_id_seq" CASCADE
;

/* Drop Tables */

DROP TABLE IF EXISTS "arp"."strategy_analytic" CASCADE
;

/* Create Tables */

CREATE TABLE "arp"."strategy_analytic"
(
	"id" serial NOT NULL,
	"strategy_id" integer NOT NULL,
	"model_instance_id" integer NOT NULL,
	"execution_state_id" integer NOT NULL,
	"business_date" date NOT NULL,
	"category" varchar(50)	 NOT NULL,
	"subcategory" varchar(50)	 NOT NULL,
	"frequency" arp.frequency NOT NULL,
	"value" numeric(32,16) NOT NULL,
	"comparator_name" varchar(50) NULL,
	"comparator_value" numeric(32, 16) NULL
)
;
/* Create Primary Keys, Indexes, Uniques, Checks */

ALTER TABLE "arp"."strategy_analytic" ADD CONSTRAINT "strategy_analytic_pkey"
	PRIMARY KEY ("id")
;

ALTER TABLE
	"arp"."strategy_analytic"
ADD CONSTRAINT
	"strategy_analytic_strategy_id__business_date_category_subcategory_key"
UNIQUE
	("strategy_id","business_date", "category","subcategory")
;

/* Create Foreign Key Constraints */

ALTER TABLE "arp"."strategy_analytic" ADD CONSTRAINT "strategy_analytic_execution_state_fkey"
	FOREIGN KEY ("execution_state_id") REFERENCES "config"."execution_state" ("id") ON DELETE No Action ON UPDATE No Action
;


ALTER TABLE "arp"."strategy_analytic" ADD CONSTRAINT "strategy_analytic_model_instance_fkey"
	FOREIGN KEY ("model_instance_id") REFERENCES "config"."model_instance" ("id") ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE "arp"."strategy_analytic" ADD CONSTRAINT "strategy_analytic_strategy_fkey"
	FOREIGN KEY ("strategy_id") REFERENCES "arp"."strategy" ("id") ON DELETE CASCADE ON UPDATE No Action
;