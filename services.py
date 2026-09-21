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

        if not rows:
            print("No members found.")
            return

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

        if not rows:
            print("No equipment found.")
            return

        for r in rows:
            e = Equipment(r["equipment_id"], r["name"], r["category"], r["is_available"])
            print(f"ID: {e.equipment_id} | Name: {e.name} | Category: {e.category} | Available: {'Yes' if e.is_available else 'No'}")

    def checkout_equipment(self, member_id, equipment_id):
        conn = get_connection()
        c = conn.cursor()

        c.execute("SELECT * FROM members WHERE member_id = ?", (member_id,))
        if not c.fetchone():
            print("Member not found.")
            conn.close()
            return

        c.execute("SELECT * FROM equipment WHERE equipment_id = ? AND is_available = 1", (equipment_id,))
        equipment = c.fetchone()
        if not equipment:
            print("Equipment not available or not found.")
            conn.close()
            return

        from datetime import date
        checkout_date = date.today().isoformat()

        c.execute(
            "INSERT INTO loans (member_id, equipment_id, checkout_date) VALUES (?, ?, ?)",
            (member_id, equipment_id, checkout_date),
        )
        c.execute("UPDATE equipment SET is_available = 0 WHERE equipment_id = ?", (equipment_id,))
        conn.commit()
        conn.close()
        print("item checked out successfully")

    def return_equipment(self, loan_id):
        conn = get_connection()
        c = conn.cursor()

        c.execute("SELECT equipment_id FROM loans WHERE loan_id = ?", (loan_id,))
        loan = c.fetchone()
        if not loan:
            print("Loan not found.")
            conn.close()
            return

        c.execute("UPDATE equipment SET is_available = 1 WHERE equipment_id = ?", (loan["equipment_id"],))
        c.execute("DELETE FROM loans WHERE loan_id = ?", (loan_id,))
        conn.commit()
        conn.close()
        print("item returned successfully")

    def search(self, query):
        query = f"%{query}%"
        conn = get_connection()
        c = conn.cursor()

        c.execute("SELECT * FROM members WHERE name LIKE ? OR email LIKE ?", (query, query))
        members = c.fetchall()

        c.execute("SELECT * FROM equipment WHERE name LIKE ? OR category LIKE ?", (query, query))
        equipment = c.fetchall()
        conn.close()

        if not members and not equipment:
            print("No matching records found.")
            return

        for row in members:
            member = Member(row["member_id"], row["name"], row["email"])
            print(member)

        for row in equipment:
            equipment_item = Equipment(row["equipment_id"], row["name"], row["category"], row["is_available"])
            print(f"Equipment: ID {equipment_item.equipment_id} | {equipment_item.name} | {equipment_item.category} | Available: {'Yes' if equipment_item.is_available else 'No'}")

    def report_active_loans(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute(
            """
            SELECT l.loan_id, m.member_id, m.name AS member_name, e.equipment_id, e.name AS equipment_name,
                   e.category, l.checkout_date
            FROM loans l
            JOIN members m ON m.member_id = l.member_id
            JOIN equipment e ON e.equipment_id = l.equipment_id
            ORDER BY l.loan_id
            """
        )
        rows = c.fetchall()
        conn.close()

        if not rows:
            print("No active loans.")
            return

        for row in rows:
            print(
                f"Loan ID: {row['loan_id']} | Member: {row['member_name']} ({row['member_id']}) | "
                f"Equipment: {row['equipment_name']} ({row['equipment_id']}) | "
                f"Category: {row['category']} | Checkout Date: {row['checkout_date']}"
            )

    def report_member_history(self, member_id):
        conn = get_connection()
        c = conn.cursor()

        c.execute("SELECT * FROM members WHERE member_id = ?", (member_id,))
        member = c.fetchone()
        if not member:
            print("Member not found.")
            conn.close()
            return

        c.execute(
            """
            SELECT l.loan_id, e.name AS equipment_name, e.category, l.checkout_date
            FROM loans l
            JOIN equipment e ON e.equipment_id = l.equipment_id
            WHERE l.member_id = ?
            ORDER BY l.checkout_date DESC
            """,
            (member_id,),
        )
        rows = c.fetchall()
        conn.close()

        print(f"History for {member['name']} ({member['email']}):")
        if not rows:
            print("No loan history found.")
            return

        for row in rows:
            print(
                f"Loan ID: {row['loan_id']} | Equipment: {row['equipment_name']} | "
                f"Category: {row['category']} | Checkout Date: {row['checkout_date']}"
            )
