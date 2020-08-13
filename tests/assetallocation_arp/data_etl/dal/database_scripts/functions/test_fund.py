from json import loads
from os import environ

from sqlalchemy import create_engine

from tests.assetallocation_arp.data_etl.dal.database_scripts.helper import run_proc

config = loads(environ['DATABASE'])
c_str = f"postgresql://{config['USER']}:{config['PASSWORD']}@{config['HOST']}:{config['PORT']}/{config['DATABASE']}"


def test_insert_fund_inserts_values_into_fund_table():
    proc_name = 'fund.insert_fund'
    proc_params = ['a', 'EUR']
    select_res = "SELECT * FROM fund.fund f JOIN lookup.currency c on f.currency_id = c.id WHERE name='a'"

    results = run_proc(create_engine(c_str), proc_name, proc_params, select_res)

    assert 1 == len(results)
    assert 'a' == results[0].get('name')
    assert 'EUR' == results[0].get('currency')


def test_insert_fund_has_execution_with_name_function_name():
    proc_name = 'fund.insert_fund'
    proc_params = ['test_fund_name', 'EUR']
    select_res = """
SELECT 
  e.name
FROM 
  config.execution e 
  JOIN config.execution_state es 
  ON es.execution_id = e.id
  JOIN fund.fund f 
  ON f.execution_state_id = es.id
WHERE f.name='test_fund_name'
"""
    results = run_proc(create_engine(c_str), proc_name, proc_params, select_res)

    assert 1 == len(results)
    assert proc_name == results[0].get('name')


def test_select_fund_returns_fund_currency():
    e = create_engine(c_str)
    conn = e.raw_connection()
    cursor = conn.cursor()

    cursor.callproc('fund.insert_fund', ['test_fund_name', 'EUR'])

    cursor.callproc('fund.select_fund', ['test_fund_name'])
    column_names_list = [x[0] for x in cursor.description]
    results = [dict(zip(column_names_list, row)) for row in cursor.fetchall()]

    conn.rollback()
    cursor.close()

    assert 1 == len(results)
    assert 'EUR' == results[0].get('currency')
