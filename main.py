from database import init_db
from services import MakerSpaceService


def safe_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input! Enter a number.")


def main():
    init_db()
    service = MakerSpaceService()

    while True:
        print("\n=== MAKERSPACE MENU ===")
        print("1. Register Member")
        print("2. List Members")
        print("3. Update Member")
        print("4. Register Equipment")
        print("5. List Equipment")
        print("6. Update Equipment")
        print("7. Checkout Equipment")
        print("8. Return Equipment")
        print("9. Search")
        print("10. Active Loans Report")
        print("11. Member History Report")
        print("0. Exit")

        choice = input("Enter choice: ").strip()

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
            m_id = safe_int("Member ID to update: ")
            new_name = input("New Name: ").strip()
            new_email = input("New Email: ").strip()
            if new_name and new_email:
                service.update_member(m_id, new_name, new_email)

        elif choice == "4":
            name = input("Equipment Name: ").strip()
            category = input("Category: ").strip()
            if name and category:
                service.add_equipment(name, category)

        elif choice == "5":
            service.list_equipment()

        elif choice == "6":
            e_id = safe_int("Equipment ID to update: ")
            new_name = input("New Equipment Name: ").strip()
            new_cat = input("New Category: ").strip()
            if new_name and new_cat:
                service.update_equipment(e_id, new_name, new_cat)

        elif choice == "7":
            m_id = safe_int("Member ID: ")
            e_id = safe_int("Equipment ID: ")
            service.checkout_equipment(m_id, e_id)

        elif choice == "8":
            l_id = safe_int("Loan ID: ")
            service.return_equipment(l_id)

        elif choice == "9":
            query = input("Search term or ID: ").strip()
            if query:
                service.search(query)

        elif choice == "10":
            service.report_active_loans()

        elif choice == "11":
            member_id = safe_int("Member ID: ")
            service.report_member_history(member_id)

        elif choice == "0":
            print("Goodbye")
            print("Exited.")
            break

        else:
            print("Invalid choice, please select 0 to 11.")


if __name__ == "__main__":
    main()