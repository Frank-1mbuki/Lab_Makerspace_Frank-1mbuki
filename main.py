from database import init_db
from services import MakerSpaceService

def safe_int(prompt):
    while True:
        try:
            val = int(input(prompt))
        except ValueError:
            print("Invalid input! Enter a number.")

def main():
    init_db()
    service = MakerSpaceService()

    while True:
        print("\n=== MAKERSPACE MENU ===")
        print("1. Register Member")
        print("2. List Members")
        print("3. Register Equipment")
        print("4. List Equipment")
        print("5. Checkout Equipment")
        print("6. Return Equipment")
        print("7. Search")
        print("8. Active Loans Report")
        print("9. Member History Report")
        print("0. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Name: ")
            email = input("Email: ")
            service.add_member(name, email)

        elif choice == "2":
            service.list_members()

        elif choice == "3":
            name = input("Equipment Name: ")
            category = input("Category: ")
            service.add_equipment(name, category)

        elif choice == "4":
            service.list_equipment()

        elif choice == "5":
            m_id = safe_int("Member ID: ")
            e_id = safe_int("Equipment ID: ")
            service.checkout_equipment(m_id, e_id)

        elif choice == "6":
            loan_id = input("Loan ID to return: ")
            service.return_equipment(loan_id)

        elif choice == "7":
            query = input("Search: ")
            service.search(query)

        elif choice == "8":
            service.report_active_loans()

        elif choice == "9":
            member_id = input("Member ID: ")
            service.report_member_history(member_id)

        elif choice == "0":
            print("Goodbye")
            print("Exited.")