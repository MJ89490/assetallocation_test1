/* ---------------------------------------------------- */
/*  Generated by Enterprise Architect Version 12.0 		*/
/*  Created On : 06-Aug-2020 10:13:38 				*/
/*  DBMS       : PostgreSQL 						*/
/* ---------------------------------------------------- */

/* Drop Tables */

DROP TABLE IF EXISTS "staging"."asset" CASCADE
;

/* Create Tables */

CREATE TABLE "staging"."asset"
(
	"id" serial NOT NULL,
	"ticker" text NOT NULL,
	"name" text	NULL,
	"description" text NULL,
	"asset_category" text NOT NULL,
	"asset_subcategory" text NOT NULL,
	"currency" text NULL,
	"country" text NULL,
	"system_datetime" timestamp with time zone NOT NULL DEFAULT now()
)
;
