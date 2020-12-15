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
	"ticker" text NOT NULL,
	"name" text	NULL,
	"description" text NULL,
	"asset_category" text NOT NULL,
	"asset_subcategory" text NOT NULL,
	"currency" text NULL,
	"country" text NULL,
	"is_tr" boolean NULL,
	"analytic_category" text NOT NULL,
	"source" text NULL,
	"value" numeric(32,16) NOT NULL,
	"business_datetime" timestamp with time zone NOT NULL,
	"system_tstzrange" tstzrange NOT NULL DEFAULT tstzrange(now(), 'infinity', '[)')
)
;
