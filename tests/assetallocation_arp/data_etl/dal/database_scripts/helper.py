from typing import List, Dict, Any

def run_proc(engine, proc_name, proc_params, select_res) -> List[Dict[str, Any]]:
    conn = engine.raw_connection()
    cursor = conn.cursor()
    cursor.callproc(proc_name, proc_params)
    cursor.execute(select_res)
    column_names_list = [x[0] for x in cursor.description]
    results = [dict(zip(column_names_list, row)) for row in cursor.fetchall()]
    conn.rollback()
    cursor.close()
    return results
