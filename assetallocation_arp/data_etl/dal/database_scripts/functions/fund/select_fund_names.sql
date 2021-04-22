CREATE OR REPLACE FUNCTION fund.select_fund_names(
  OUT fund_names varchar[]
)
AS
$$
BEGIN
  SELECT array_agg(f.name) from fund.fund f INTO fund_names
  ;
END;
$$
LANGUAGE plpgsql;