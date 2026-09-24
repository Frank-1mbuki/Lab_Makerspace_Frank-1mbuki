import sqlite3
from datetime import datetime
from database import get_connection
from models import Member, Equipment, Loan


class MakerSpaceService:

    def add_member(self, name, email):
        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute("INSERT INTO members (name, email) VALUES (?, ?)", (name, email))
            conn.commit()
            print("added member!")
        except sqlite3.IntegrityError:
            print("Error: Member with this email already exists.")
        finally:
            conn.close()

    def list_members(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM members")
        rows = c.fetchall()
        conn.close()

        if not rows:
            print("No members found.")
            return

        for r in rows:
            m = Member(r["member_id"], r["name"], r["email"])
            print(m)

    def update_member(self, member_id, new_name, new_email):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM members WHERE member_id = ?", (member_id,))
        if not c.fetchone():
            print("Error: Member not found!")
            conn.close()
            return

        c.execute("UPDATE members SET name = ?, email = ? WHERE member_id = ?", (new_name, new_email, member_id))
        conn.commit()
        conn.close()
        print("member updated successfully!")

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

        if not rows:
            print("No equipment found.")
            return

        for r in rows:
            eq = Equipment(r["equipment_id"], r["name"], r["category"], r["is_available"])
            print(eq)

    def update_equipment(self, equipment_id, new_name, new_category):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM equipment WHERE equipment_id = ?", (equipment_id,))
        if not c.fetchone():
            print("Error: Equipment not found!")
            conn.close()
            return

        c.execute("UPDATE equipment SET name = ?, category = ? WHERE equipment_id = ?", (new_name, new_category, equipment_id))
        conn.commit()
        conn.close()
        print("equipment updated successfully!")

    def checkout_equipment(self, member_id, equipment_id):
        """Check out equipment only when both records exist and the item is available."""
        conn = get_connection()
        c = conn.cursor()

        # Validate the member first so a loan can never reference a missing member.
        c.execute("SELECT member_id FROM members WHERE member_id = ?", (member_id,))
        if c.fetchone() is None:
            print("Error: Member not found. Checkout cancelled.")
            conn.close()
            return

        # Fetching the equipment row also distinguishes a missing item from a borrowed one.
        c.execute("SELECT equipment_id, is_available FROM equipment WHERE equipment_id = ?", (equipment_id,))
        item = c.fetchone()
        if item is None:
            print("Error: Equipment not found. Checkout cancelled.")
            conn.close()
            return

        if item["is_available"] == 0:
            print("Error: Equipment is already borrowed!")
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

        c.execute("SELECT * FROM loans WHERE loan_id = ? AND is_active = 1", (loan_id,))
        loan = c.fetchone()

        if not loan:
            print("Error: Active loan not found!")
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
        m_rows = c.fetchall()
        if not m_rows:
            print("No matching members found.")
        else:
            for r in m_rows:
                print(Member(r["member_id"], r["name"], r["email"]))

        print("\n--- Equipment Found ---")
        c.execute("SELECT * FROM equipment WHERE name LIKE ? OR equipment_id = ?", (f"%{query}%", query))
        e_rows = c.fetchall()
        if not e_rows:
            print("No matching equipment found.")
        else:
            for r in e_rows:
                print(Equipment(r["equipment_id"], r["name"], r["category"], r["is_available"]))

        conn.close()

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

    def report_member_history(self, member_id):
        conn = get_connection()
        c = conn.cursor()
        query = """
            SELECT l.loan_id, e.name as equipment_name, l.checkout_date, l.return_date, l.is_active
            FROM loans l
            JOIN equipment e ON l.equipment_id = e.equipment_id
            WHERE l.member_id = ?
        """
        c.execute(query, (member_id,))
        rows = c.fetchall()
        conn.close()

        print(f"\n--- Loan History for Member #{member_id} ---")
        if not rows:
            print("No loans found for this member.")
            return

        for r in rows:
            status = "Active" if r["is_active"] else f"Returned on {r['return_date']}"
            print(f"Loan ID: {r['loan_id']} | Item: {r['equipment_name']} | Date: {r['checkout_date']} | Status: {status}")
