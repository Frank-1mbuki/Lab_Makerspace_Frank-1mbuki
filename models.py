class Member:
    def __init__(self, member_id, name, email):
        self.member_id = member_id
        self.name = name
        self.email = email

class Equipment:
    def __init__(self, equipment_id, name, category, status):
        self.equipment_id = equipment_id
        self.name = name
        self.category = category
        self.status = status

class Loan:
    def __init__(self, loan_id, member_id, equipment_id, checkout_date):
        self.loan_id = loan_id
        self.member_id = member_id
        self.equipment_id = equipment_id
        self.checkout_date = checkout_date