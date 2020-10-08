CREATE OR REPLACE FUNCTION curve.insert_tickers(
  execution_state_id int,
  tickers curve.ticker_months_years[],
  OUT ticker_ids int[]
)
AS
$$
BEGIN
  WITH input_rows as(
     SELECT
      insert_tickers.execution_state_id,
      (t).category as category,
      (t).mth3 as mth3,
      (t).yr1 as yr1,
      (t).yr2 as yr2,
      (t).yr3 as yr3,
      (t).yr4 as yr4,
      (t).yr5 as yr5,
      (t).yr6 as yr6,
      (t).yr7 as yr7,
      (t).yr8 as yr8,
      (t).yr9 as yr9,
      (t).yr10 as yr10,
      (t).yr15 as yr15,
      (t).yr20 as yr20,
      (t).yr30 as yr30
    FROM
      unnest(tickers) as t
  ),
  ins as (
      INSERT INTO curve.ticker (execution_state_id, category, mth3, yr1, yr2, yr3, yr4, yr5, yr6, yr7, yr8, yr9, yr10, yr15, yr20, yr30)
      SELECT * from input_rows
      ON CONFLICT (category, mth3, yr1, yr2, yr3, yr4, yr5, yr6, yr7, yr8, yr9, yr10, yr15, yr20, yr30) DO NOTHING
      RETURNING curve.ticker.id
  )
  SELECT id
  FROM ins
  UNION ALL
  SELECT t.id
  FROM ticker t JOIN input_rows i USING(category, mth3, yr1, yr2, yr3, yr4, yr5, yr6, yr7, yr8, yr9, yr10, yr15, yr20, yr30)
  into ticker_ids;
  RETURN;
END;
$$
LANGUAGE plpgsql;
