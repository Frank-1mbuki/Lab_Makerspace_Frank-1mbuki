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
            name = input("Name: ").strip()
            email = input("Email: ").strip()
            if name and email:
                service.add_member(name, email)
            else:
                print("Name and email cannot be empty.")

        elif choice == "2":
            service.list_members()

        elif choice == "3":
            name = input("Equipment Name: ")
            category = input("Category: ")
            service.add_equipment(name, category)

        elif choice == "4":
            service.list_equipment()

        elif choice == "5":
            m_id = input("Member ID: ").strip()
            e_id = input("Equipment ID: ").strip()
            if m_id and e_id:
                service.checkout_equipment(int(m_id), int(e_id))

        elif choice == "6":
            l_id = input("Loan ID: ").strip()
            if l_id:
                service.return_equipment(int(l_id))

        elif choice == "7":
            query = input("Search term or ID: ").strip()
            if query:
                service.search(query)
                
        elif choice == "8":
            service.report_active_loans()

        elif choice == "9":
            member_id = input("Member ID: ")
            service.report_member_history(member_id)

        elif choice == "0":
            print("Goodbye")
            print("Exited.")

if __name__ == "__main__":
    main()
