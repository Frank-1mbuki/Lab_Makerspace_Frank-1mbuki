import sqlite3
from database import get_connection
from models import Member

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
