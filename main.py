from database import init_db
from services import MakerSpaceService


def safe_int(prompt):
    """Read a positive integer without allowing invalid input to crash the app."""
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
            if number <= 0:
                print("Invalid input! Enter a positive number.")
                continue
            return number
        except (TypeError, ValueError):
            print("Invalid input! Enter a whole number.")


def safe_name(prompt):
    """Read a non-empty name containing only letters and common name separators."""
    while True:
        name = input(prompt).strip()
        if not name:
            print("Name cannot be empty.")
            continue

        if all(character.isalpha() or character in " '-" for character in name):
            return name

        print("Invalid name! Use letters, spaces, apostrophes, or hyphens only.")


def main():
    init_db()
    service = MakerSpaceService()

    try:
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
                name = safe_name("Name: ")
                email = input("Email: ").strip()
                if email:
                    service.add_member(name, email)
                else:
                    print("Email cannot be empty.")

            elif choice == "2":
                service.list_members()

            elif choice == "3":
                m_id = safe_int("Member ID to update: ")
                new_name = input("New Name: ").strip()
                new_email = input("New Email: ").strip()
                if new_name and new_email:
                    service.update_member(m_id, new_name, new_email)
                else:
                    print("Name and email cannot be empty.")

            elif choice == "4":
                name = input("Equipment Name: ").strip()
                category = input("Category: ").strip()
                if name and category:
                    service.add_equipment(name, category)
                else:
                    print("Equipment name and category cannot be empty.")

            elif choice == "5":
                service.list_equipment()

            elif choice == "6":
                e_id = safe_int("Equipment ID to update: ")
                new_name = input("New Equipment Name: ").strip()
                new_cat = input("New Category: ").strip()
                if new_name and new_cat:
                    service.update_equipment(e_id, new_name, new_cat)
                else:
                    print("Equipment name and category cannot be empty.")

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
                else:
                    print("Search term cannot be empty.")

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
                print("Invalid choice. Please select a menu option from 0 to 11.")
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled. Goodbye.")


if __name__ == "__main__":
    main()
