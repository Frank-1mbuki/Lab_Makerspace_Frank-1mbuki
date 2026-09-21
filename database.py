import sqlite3

def get_connection():
    conn = sqlite3.connect("makerspace.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS members (member_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS equipment (equipment_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, category TEXT, is_available INTEGER DEFAULT 1)")
    c.execute("CREATE TABLE IF NOT EXISTS loans (loan_id INTEGER PRIMARY KEY AUTOINCREMENT, member_id INT, equipment_id INT, checkout_date TEXT)")
    conn.commit()
    conn.close()
