from json import loads
from os import environ

from sqlalchemy import create_engine

from tests.assetallocation_arp.data_etl.dal.resources import valid_times, valid_fica

config = loads(environ['DATABASE'])
c_str = f"postgresql://{config['USER']}:{config['PASSWORD']}@{config['HOST']}:{config['PORT']}/{config['DATABASE']}"


def test_insert_times_strategy_inserts_values_into_times_table(valid_times):
    # setup
    conn = create_engine(c_str).raw_connection()
    cursor = conn.cursor()
    cursor.callproc('config.insert_execution_state', ['arp.insert_times_strategy'])
    es_id = cursor.fetchone()[0]
    cursor.execute(f"INSERT INTO arp.app_user (id, name, execution_state_id) VALUES ('test_u', 'test', {es_id})")

    # function to test
    cursor.callproc('arp.insert_times_strategy',
                    [valid_times.description, 'test_u', valid_times.time_lag_interval, valid_times.leverage_type,
                     valid_times.volatility_window, valid_times.short_signals, valid_times.long_signals,
                     valid_times.frequency, valid_times.day_of_week])

    # get results
    cursor.execute("""
    SELECT 
      CAST(t.time_lag AS VARCHAR) as time_lag_interval, 
      t.leverage_type, 
      t.volatility_window, 
      t.short_signals, 
      t.long_signals, 
      t.frequency, 
      t.day_of_week
    FROM 
      arp.strategy s 
      JOIN arp.times t ON s.id = t.strategy_id
    WHERE 
      s.name='times'
      AND upper(s.system_tstzrange) = 'infinity'
    """)
    column_names_list = [x[0] for x in cursor.description]
    results = [dict(zip(column_names_list, row)) for row in cursor.fetchall()]
    conn.rollback()
    cursor.close()

    # compare to expected
    assert 1 == len(results)
    assert valid_times.time_lag_interval == results[0].get('time_lag_interval')
    assert valid_times.leverage_type == results[0].get('leverage_type')
    assert valid_times.volatility_window == results[0].get('volatility_window')
    assert valid_times.short_signals == results[0].get('short_signals')
    assert valid_times.long_signals == results[0].get('long_signals')
    assert valid_times.frequency == results[0].get('frequency')
    assert valid_times.day_of_week == results[0].get('day_of_week')


def test_insert_times_strategy_creates_execution_state_with_function_name(valid_times):
    # setup
    conn = create_engine(c_str).raw_connection()
    cursor = conn.cursor()
    cursor.callproc('config.insert_execution_state', ['arp.insert_times_strategy'])
    es_id = cursor.fetchone()[0]
    cursor.execute(f"INSERT INTO arp.app_user (id, name, execution_state_id) VALUES ('test_u', 'test', {es_id})")

    # function to test
    proc_name = 'arp.insert_times_strategy'
    cursor.callproc(proc_name,
                    [valid_times.description, 'test_u', valid_times.time_lag_interval, valid_times.leverage_type,
                     valid_times.volatility_window, valid_times.short_signals, valid_times.long_signals,
                     valid_times.frequency, valid_times.day_of_week])

    # get results
    cursor.execute("""
    SELECT 
      e.name
    FROM 
      config.execution e 
      JOIN config.execution_state es 
      ON es.execution_id = e.id
      JOIN arp.strategy s 
      ON s.execution_state_id = es.id
    WHERE 
      s.name='times'
      AND upper(s.system_tstzrange) = 'infinity'
    """)
    column_names_list = [x[0] for x in cursor.description]
    results = [dict(zip(column_names_list, row)) for row in cursor.fetchall()]
    conn.rollback()
    cursor.close()

    assert 1 == len(results)
    assert proc_name == results[0].get('name')


def test_insert_times_strategy_closes_previous_record_so_only_one_record_has_upper_system_tstzrange_of_infinity(
        valid_times):
    # setup
    conn = create_engine(c_str).raw_connection()
    cursor = conn.cursor()
    cursor.callproc('config.insert_execution_state', ['arp.insert_times_strategy'])
    es_id = cursor.fetchone()[0]
    cursor.execute(f"INSERT INTO arp.app_user (id, name, execution_state_id) VALUES ('test_u', 'test', {es_id})")

    # function to test
    proc_name = 'arp.insert_times_strategy'
    cursor.callproc(proc_name,
                    [valid_times.description, 'test_u', valid_times.time_lag_interval, valid_times.leverage_type,
                     valid_times.volatility_window, valid_times.short_signals, valid_times.long_signals,
                     valid_times.frequency, valid_times.day_of_week])

    # get results
    cursor.execute("""
    SELECT 
      *
    FROM 
      arp.strategy s 
    WHERE 
      s.name='times'
      AND upper(s.system_tstzrange) = 'infinity'
    """)
    column_names_list = [x[0] for x in cursor.description]
    results = [dict(zip(column_names_list, row)) for row in cursor.fetchall()]
    conn.rollback()
    cursor.close()

    assert 1 == len(results)


def test_insert_fica_strategy_inserts_values_into_fica_table(valid_fica):
    # setup
    conn = create_engine(c_str).raw_connection()
    cursor = conn.cursor()
    cursor.callproc('config.insert_execution_state', ['arp.insert_fica_strategy'])
    es_id = cursor.fetchone()[0]
    cursor.execute(f"INSERT INTO arp.app_user (id, name, execution_state_id) VALUES ('test_u', 'test', {es_id})")

    # function to test
    cursor.callproc('arp.insert_fica_strategy',
                    [valid_fica.description, 'test_u', valid_fica.coupon, valid_fica.curve, valid_fica.business_tstzrange,
                              valid_fica.strategy_weights, valid_fica.tenor, valid_fica.trading_cost])

    # get results
    cursor.execute("""
    SELECT 
      s.description, 
      t.coupon, 
      t.curve, 
      t.business_tstzrange, 
      t.strategy_weights, 
      t.tenor, 
      t.trading_cost
    FROM 
      arp.strategy s 
      JOIN arp.fica t ON s.id = t.strategy_id
    WHERE 
      s.name='fica'
      AND upper(s.system_tstzrange) = 'infinity'
    """)
    column_names_list = [x[0] for x in cursor.description]
    results = [dict(zip(column_names_list, row)) for row in cursor.fetchall()]
    conn.rollback()
    cursor.close()

    # compare to expected
    assert 1 == len(results)
    assert valid_fica.description == results[0].get('description')
    assert valid_fica.coupon == results[0].get('coupon')
    assert valid_fica.curve == results[0].get('curve')
    assert valid_fica.strategy_weights == results[0].get('strategy_weights')
    assert valid_fica.tenor == results[0].get('tenor')
    assert valid_fica.trading_cost == results[0].get('trading_cost')
    assert valid_fica.business_tstzrange == results[0].get('business_tstzrange')