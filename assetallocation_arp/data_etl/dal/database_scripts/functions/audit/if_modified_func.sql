CREATE OR REPLACE FUNCTION audit.if_modified_func() RETURNS TRIGGER AS $body$
DECLARE
    audit_row audit.logged_action;
    excluded_cols text[] = ARRAY[]::text[];
BEGIN
    audit_row.schema_name = TG_TABLE_SCHEMA::text;
    audit_row.table_name = TG_TABLE_NAME::text;
    audit_row.session_user_name = session_user::text;
    audit_row.action_tstamp_tx = current_timestamp;
    audit_row.action_tstamp_stm = statement_timestamp();
    audit_row.transaction_id = txid_current();
    audit_row.action = substring(TG_OP,1,1);
    audit_row.row_data = NULL;
    audit_row.changed_fields = NULL;
    audit_row.statement_only = 'f';


    IF TG_ARGV[1] IS NOT NULL THEN
        excluded_cols = TG_ARGV[1]::text[];
    END IF;

    IF (TG_OP = 'UPDATE' AND TG_LEVEL = 'ROW') THEN
        audit_row.row_data = to_jsonb(OLD.*) #- excluded_cols;
        audit_row.changed_fields =  (audit.jsonb_minus(to_jsonb(NEW.*), audit_row.row_data)) #- excluded_cols;
        IF audit_row.changed_fields = '"{}"' THEN
            -- All changed fields are ignored. Skip this update.
            RETURN NULL;
        END IF;
    ELSIF (TG_OP = 'DELETE' AND TG_LEVEL = 'ROW') THEN
        audit_row.row_data = to_jsonb(OLD.*) #- excluded_cols;
    ELSIF (TG_OP = 'INSERT' AND TG_LEVEL = 'ROW') THEN
        RETURN NULL;
    ELSIF (TG_LEVEL = 'STATEMENT' AND TG_OP IN ('INSERT','UPDATE','DELETE','TRUNCATE')) THEN
        audit_row.statement_only = 't';
    ELSE
        RAISE EXCEPTION '[audit.if_modified_func] - Trigger func added as trigger for unhandled case: %, %',TG_OP, TG_LEVEL;
        RETURN NULL;
    END IF;
    INSERT INTO audit.logged_action (
        schema_name,
        table_name,
        session_user_name,
        action_tstamp_tx,
        action_tstamp_stm,
        transaction_id,
        application_name,
        action,
        row_data,
        changed_fields,
        statement_only
    ) VALUES (
        audit_row.schema_name,
        audit_row.table_name,
        audit_row.session_user_name,
        audit_row.action_tstamp_tx,
        audit_row.action_tstamp_stm,
        audit_row.transaction_id,
        audit_row.application_name,
        audit_row.action,
        audit_row.row_data,
        audit_row.changed_fields,
        audit_row.statement_only
    );
    RETURN NULL;
END;
$body$
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = pg_catalog, public;

COMMENT ON FUNCTION audit.if_modified_func() IS $body$
Track changes to a table at the statement and/or row level.

Optional parameters to trigger in CREATE TRIGGER call:

param 0: boolean, whether to log the query text. Default 't'.

param 1: text[], columns to ignore in updates. Default [].

         Updates to ignored cols are omitted from changed_fields.

         Updates with only ignored cols changed are not inserted
         into the audit log.

         Almost all the processing work is still done for updates
         that ignored. If you need to save the load, you need to use
         WHEN clause on the trigger instead.

         No warning or error is issued if ignored_cols contains columns
         that do not exist in the target table. This lets you specify
         a standard set of ignored columns.

There is no parameter to disable logging of values. Add this trigger as
a 'FOR EACH STATEMENT' rather than 'FOR EACH ROW' trigger if you do not
want to log row values.

Note that the user name logged is the login role for the session. The audit trigger
cannot obtain the active role because it is reset by the SECURITY DEFINER invocation
of the audit trigger its self.
$body$;