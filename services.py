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

def checkout_equipment(self, member_id, equipment_id):
        conn = get_connection()
        c = conn.cursor()

        c.execute("SELECT is_available FROM equipment WHERE equipment_id = ?", (equipment_id,))
        item = c.fetchone()

        if not item:
            print("Equipment not found!")
            conn.close()
            return

        if item["is_available"] == 0:
            print("Equipment is already borrowed!")
            conn.close()
            return

        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO loans (member_id, equipment_id, checkout_date) VALUES (?, ?, ?)", (member_id, equipment_id, date_now))
        c.execute("UPDATE equipment SET is_available = 0 WHERE equipment_id = ?", (equipment_id,))
        conn.commit()
        conn.close()
        print("item checked out successfully!")