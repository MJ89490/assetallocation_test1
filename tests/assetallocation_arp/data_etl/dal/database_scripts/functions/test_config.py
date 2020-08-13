from json import loads
from os import environ

from sqlalchemy import create_engine

config = loads(environ['DATABASE'])
c_str = f"postgresql://{config['USER']}:{config['PASSWORD']}@{config['HOST']}:{config['PORT']}/{config['DATABASE']}"


def test_insert_execution_state_inserts_values_into_execution_state_table():
    e = create_engine(c_str)
    conn = e.raw_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO config.execution (name, in_use) VALUES ('test_insert_execution_state', 't')")

    cursor.callproc('config.insert_execution_state', ['test_insert_execution_state'])

    cursor.execute("""
SELECT 
  e.name
FROM 
  config.execution e 
  JOIN config.execution_state es 
  ON es.execution_id = e.id
WHERE es.system_datetime=now()
""")
    column_names_list = [x[0] for x in cursor.description]
    results = [dict(zip(column_names_list, row)) for row in cursor.fetchall()]

    conn.rollback()
    cursor.close()

    assert 1 == len(results)
    assert 'test_insert_execution_state' == results[0].get('name')
