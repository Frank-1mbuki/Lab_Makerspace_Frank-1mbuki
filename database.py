import sqlite3

def get_connection():
    return sqlite3.connect("makerspace.db")

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS members (id INT, name TEXT, email TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS equipment (id INT, name TEXT, category TEXT, status TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS loans (id INT, member_id INT, equipment_id INT, date TEXT)")
    conn.commit()
    conn.close()