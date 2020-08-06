/* Drop Tables */

DROP TABLE IF EXISTS "asset"."asset" CASCADE
;

DROP TABLE IF EXISTS "asset"."asset_analytic" CASCADE
;

DROP TABLE IF EXISTS "lookup"."country" CASCADE
;

DROP TABLE IF EXISTS "lookup"."currency" CASCADE
;

DROP TABLE IF EXISTS "arp"."effect_asset" CASCADE
;

DROP TABLE IF EXISTS "arp"."effect" CASCADE
;

DROP TABLE IF EXISTS "arp"."fica_asset" CASCADE
;

DROP TABLE IF EXISTS "arp"."fica" CASCADE
;

DROP TABLE IF EXISTS "fund"."fund" CASCADE
;

DROP TABLE IF EXISTS "arp"."fund_strategy_asset_weight" CASCADE
;

DROP TABLE IF EXISTS "arp"."fund_strategy" CASCADE
;

DROP TABLE IF EXISTS "lookup"."source" CASCADE
;

DROP TABLE IF EXISTS "arp"."strategy" CASCADE
;

DROP TABLE IF EXISTS "arp"."strategy_asset_analytic" CASCADE
;

DROP TABLE IF EXISTS "arp"."times_asset" CASCADE
;

DROP TABLE IF EXISTS "arp"."app_user" CASCADE
;

DROP TABLE IF EXISTS "arp"."times" CASCADE
;

DROP TABLE IF EXISTS "audit"."logged_action" CASCADE
;

DROP TABLE IF EXISTS "curve"."ticker" CASCADE
;

DROP TABLE IF EXISTS "config"."execution" CASCADE
;

DROP TABLE IF EXISTS "config"."execution_state" CASCADE
;