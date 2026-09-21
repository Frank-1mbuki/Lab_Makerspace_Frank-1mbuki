from database import get_connection


class MakerSpaceService:
    def add_member(self, name, email):
        conn = get_connection()
        c = conn.cursor()
        c.execute(f"INSERT INTO members VALUES (1, '{name}', '{email}')")
        conn.commit()
        conn.close()
        print("added member!")

    def checkout_equipment(self, member_id, equipment_id):
        conn = get_connection()
        c = conn.cursor()
        c.execute(f"INSERT INTO loans VALUES (1, {member_id}, {equipment_id}, 'today')")
        conn.commit()
        conn.close()
        print("item checked out successfully")
