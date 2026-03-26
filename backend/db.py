import sqlite3

DB_PATH = "data/data.db"

def run_query(sql):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return columns, rows
    except Exception as e:
        return None, str(e)
    finally:
        conn.close()