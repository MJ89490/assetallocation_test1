/* ---------------------------------------------------- */
/*  Generated by Enterprise Architect Version 12.0 		*/
/*  Created On : 06-Aug-2020 10:13:40 				*/
/*  DBMS       : PostgreSQL 						*/
/* ---------------------------------------------------- */

/* Drop Sequences for Autonumber Columns */

DROP SEQUENCE IF EXISTS "config"."model_instance_id_seq" CASCADE
;

/* Drop Tables */

DROP TABLE IF EXISTS "config"."model_instance" CASCADE
;

/* Create Tables */

CREATE TABLE "config"."model_instance"
(
	"id" serial NOT NULL,
  "model_id" integer NOT NULL,
	"execution_state_id" integer NOT NULL,
  "python_code_version" varchar(50) NOT NULL,
  "business_daterange" daterange NOT NULL,
  "system_datetime" timestamp with time zone NOT NULL DEFAULT now()
)
;

/* Create Primary Keys, Indexes, Uniques, Checks */

ALTER TABLE "config"."model_instance" ADD CONSTRAINT "model_instance_pkey"
	PRIMARY KEY ("id")
;

/* Create Foreign Key Constraints */

ALTER TABLE "config"."model_instance" ADD CONSTRAINT "model_instance_model_fkey"
	FOREIGN KEY ("model_id") REFERENCES "config"."model" ("id") ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE "config"."model_instance" ADD CONSTRAINT "model_instance_execution_state_fkey"
	FOREIGN KEY ("execution_state_id") REFERENCES "config"."execution_state" ("id") ON DELETE No Action ON UPDATE No Action
;