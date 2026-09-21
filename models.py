class Member:
    def __init__(self, member_id, name, email):
        self.member_id = member_id
        self.name = name
        self.email = email

    def __str__(self):
        return f"ID: {self.member_id} | Name: {self.name} | Email: {self.email}"

class Equipment:
    def __init__(self, equipment_id, name, category, is_available=1):
        self.equipment_id = equipment_id
        self.name = name
        self.category = category
        self.is_available = is_available

    def __str__(self):
        status = "Available" if self.is_available else "Borrowed"
        return f"ID: {self.equipment_id} | Name: {self.name} | Category: {self.category} | Status: {status}"
