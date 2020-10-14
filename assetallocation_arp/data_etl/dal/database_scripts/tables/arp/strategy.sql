/* ---------------------------------------------------- */
/*  Generated by Enterprise Architect Version 12.0 		*/
/*  Created On : 06-Aug-2020 10:13:39 				*/
/*  DBMS       : PostgreSQL 						*/
/* ---------------------------------------------------- */

/* Drop Sequences for Autonumber Columns */

DROP SEQUENCE IF EXISTS "arp"."strategy_id_seq" CASCADE
;

/* Drop Tables */

DROP TABLE IF EXISTS "arp"."strategy" CASCADE
;

/* Create Tables */

CREATE TABLE "arp"."strategy"
(
	"id" serial NOT NULL,
	"name" varchar(50)	 NOT NULL,
	"description" varchar(100)	 NULL,
	"app_user_id" varchar(7)	 NOT NULL,
	"system_tstzrange" tstzrange NOT NULL DEFAULT tstzrange(now(), 'infinity', '[)'),
	"execution_state_id" integer NOT NULL
)
;

/* Create Primary Keys, Indexes, Uniques, Checks */

ALTER TABLE "arp"."strategy" ADD CONSTRAINT "strategy_pkey"
	PRIMARY KEY ("id")
;

-- ALTER TABLE "arp"."strategy" ADD CONSTRAINT "strategy_name_system_tstzrange_excl" EXCLUDE USING GIST (name WITH =, system_tstzrange WITH &&)

ALTER TABLE "arp"."strategy" ADD CONSTRAINT "strategy_name_check" CHECK (name in ('times', 'effect', 'fica'))
;

/* Create Foreign Key Constraints */

ALTER TABLE "arp"."strategy" ADD CONSTRAINT "strategy_execution_state_fkey"
	FOREIGN KEY ("execution_state_id") REFERENCES "config"."execution_state" ("id") ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE "arp"."strategy" ADD CONSTRAINT "strategy_user_fkey"
	FOREIGN KEY ("app_user_id") REFERENCES "arp"."app_user" ("id") ON DELETE No Action ON UPDATE No Action
;