/* ---------------------------------------------------- */
/*  Generated by Enterprise Architect Version 12.0 		*/
/*  Created On : 06-Aug-2020 10:13:40 				*/
/*  DBMS       : PostgreSQL 						*/
/* ---------------------------------------------------- */

/* Drop Tables */

DROP TABLE IF EXISTS "arp"."app_user" CASCADE
;

/* Create Tables */

CREATE TABLE "arp"."app_user"
(
	"id" varchar	 NOT NULL,
	"name" varchar(100)	 NOT NULL,
	"email" varchar(200)	 NULL,
	"execution_state_id" integer NOT NULL
)
;

/* Create Primary Keys, Indexes, Uniques, Checks */

ALTER TABLE "arp"."app_user" ADD CONSTRAINT "user_pkey"
	PRIMARY KEY ("id")
;

ALTER TABLE "arp"."app_user" ADD CONSTRAINT "user_email_key" UNIQUE ("email")
;

/* Create Foreign Key Constraints */

ALTER TABLE "arp"."app_user" ADD CONSTRAINT "FK_app_user_execution_state"
	FOREIGN KEY ("execution_state_id") REFERENCES "config"."execution_state" ("id") ON DELETE No Action ON UPDATE No Action
;