import sqlite3
from database import get_connection
from models import Member, Equipment

class MakerSpaceService:

    def add_member(self, name, email):
        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO members (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        conn.close()
        print("added member!")

    def list_members(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM members")
        rows = c.fetchall()
        conn.close()

        for r in rows:
            m = Member(r["member_id"], r["name"], r["email"])
            print(m)

    def add_equipment(self, name, category):
        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO equipment (name, category) VALUES (?, ?)", (name, category))
        conn.commit()
        conn.close()
        print("added equipment!")

    def list_equipment(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM equipment")
        rows = c.fetchall()
        conn.close()

        for r in rows:
            eq = Equipment(r["equipment_id"], r["name"], r["category"], r["is_available"])
            print(eq)
