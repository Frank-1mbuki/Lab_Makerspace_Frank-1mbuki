import sqlite3
from datetime import datetime
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

    def report_active_loans(self):
        conn = get_connection()
        c = conn.cursor()
        query = """
            SELECT l.loan_id, m.name as member_name, e.name as equipment_name, l.checkout_date
            FROM loans l
            JOIN members m ON l.member_id = m.member_id
            JOIN equipment e ON l.equipment_id = e.equipment_id
            WHERE l.is_active = 1
        """
        c.execute(query)
        rows = c.fetchall()
        conn.close()

        print("\n--- Currently Active Loans ---")
        if not rows:
            print("No active loans.")
            return

        for r in rows:
            print(f"Loan ID: {r['loan_id']} | Item: {r['equipment_name']} | Borrower: {r['member_name']} | Date: {r['checkout_date']}")

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

    def return_equipment(self, loan_id):
        conn = get_connection()
        c = conn.cursor()

        c.execute("SELECT * FROM loans WHERE loan_id = ?", (loan_id,))
        loan = c.fetchone()

        if not loan:
            print("Loan not found!")
            conn.close()
            return

        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("UPDATE loans SET return_date = ?, is_active = 0 WHERE loan_id = ?", (date_now, loan_id))
        c.execute("UPDATE equipment SET is_available = 1 WHERE equipment_id = ?", (loan["equipment_id"],))
        conn.commit()
        conn.close()
        print("item returned successfully!")

    def search(self, query):
        conn = get_connection()
        c = conn.cursor()

        print("\n--- Members Found ---")
        c.execute("SELECT * FROM members WHERE name LIKE ? OR member_id = ?", (f"%{query}%", query))
        for r in c.fetchall():
            print(Member(r["member_id"], r["name"], r["email"]))

        print("\n--- Equipment Found ---")
        c.execute("SELECT * FROM equipment WHERE name LIKE ? OR equipment_id = ?", (f"%{query}%", query))
        for r in c.fetchall():
            print(Equipment(r["equipment_id"], r["name"], r["category"], r["is_available"]))

        conn.close()
