/* ---------------------------------------------------- */
/*  Generated by Enterprise Architect Version 12.0 		*/
/*  Created On : 06-Aug-2020 10:13:38 				*/
/*  DBMS       : PostgreSQL 						*/
/* ---------------------------------------------------- */

/* Drop Sequences for Autonumber Columns */

DROP SEQUENCE IF EXISTS "asset"."asset_id_seq" CASCADE
;

/* Drop Tables */

DROP TABLE IF EXISTS "asset"."asset" CASCADE
;

/* Create Tables */

CREATE TABLE "asset"."asset"
(
	"id" serial NOT NULL,
	"spot_code" varchar(50)	 NULL,
	"name" varchar(50)	 NOT NULL,
	"ndf_code" varchar(50)	 NULL,
	"description" varchar(100)	 NULL,
	"generic_yield_ticker" varchar(50)	 NULL,
	"currency_id" integer NOT NULL,
	"country_id" integer NOT NULL,
	"category" varchar(50)	 NOT NULL,
	"execution_state_id" integer NOT NULL,
	"type" varchar(50)	 NOT NULL,
	"is_tr" boolean NOT NULL,
	"ticker" varchar(50)	 NOT NULL
)
;

/* Create Primary Keys, Indexes, Uniques, Checks */

ALTER TABLE "asset"."asset" ADD CONSTRAINT "asset_pkey"
	PRIMARY KEY ("id")
;

ALTER TABLE "asset"."asset" ADD CONSTRAINT "asset_ticker_key" UNIQUE ("ticker")
;

ALTER TABLE "asset"."asset" ADD CONSTRAINT "asset_category_check" CHECK (category in ('Equity', 'Fixed Income', 'FX', 'Commodity', 'Credit'))
;

/* Create Foreign Key Constraints */

ALTER TABLE "asset"."asset" ADD CONSTRAINT "asset_country_fkey"
	FOREIGN KEY ("country_id") REFERENCES "lookup"."country" ("id") ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE "asset"."asset" ADD CONSTRAINT "asset_currency_fkey"
	FOREIGN KEY ("currency_id") REFERENCES "lookup"."currency" ("id") ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE "asset"."asset" ADD CONSTRAINT "asset_execution_state_fkey"
	FOREIGN KEY ("execution_state_id") REFERENCES "config"."execution_state" ("id") ON DELETE No Action ON UPDATE No Action
;