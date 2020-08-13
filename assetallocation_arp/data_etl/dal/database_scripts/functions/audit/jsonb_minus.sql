CREATE OR REPLACE FUNCTION jsonb_minus ( arg1 jsonb, arg2 jsonb )
 RETURNS jsonb
AS $$

SELECT
	COALESCE(json_object_agg(
        key,
        CASE
            -- if the value is an object and the value of the second argument is
            -- not null, we do a recursion
            WHEN jsonb_typeof(value) = 'object' AND arg2 -> key IS NOT NULL
			THEN jsonb_minus(value, arg2 -> key)
            -- for all the other types, we just return the value
            ELSE value
        END
    ), '{}')::jsonb
FROM
	jsonb_each(arg1)
WHERE
	arg1 -> key <> arg2 -> key
	OR arg2 -> key IS NULL

$$ LANGUAGE SQL;