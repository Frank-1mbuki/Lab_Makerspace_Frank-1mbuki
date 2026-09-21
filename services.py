from database import get_connection

class MakerSpaceService:
    def add_member(self, name, email):
        conn = get_connection()
        c = conn.cursor()
        c.execute(f"INSERT INTO members VALUES (1, '{name}', '{email}')")
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
            print(Member(r["member_id"], r["name"], r["email"]))
