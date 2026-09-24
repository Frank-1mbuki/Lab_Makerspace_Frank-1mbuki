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


def safe_name(prompt, field_name="Name"):
    """Read a valid person name with letters and common separators only."""
    while True:
        value = input(prompt).strip()
        if not value:
            print(f"{field_name} cannot be empty.")
            continue

        if all(character.isalpha() or character in " '-" for character in value):
            return value

        print(f"Invalid {field_name.lower()}! Use letters, spaces, apostrophes, or hyphens only.")


def safe_email(prompt):
    """Read a valid email address and keep looping until it passes basic checks."""
    while True:
        email = input(prompt).strip()
        if not email:
            print("Email cannot be empty.")
            continue

        if "@" in email and email.count("@") == 1:
            local_part, domain = email.split("@", 1)
            if local_part and "." in domain and domain.replace(".", "").isalpha() is False:
                return email

        print("Invalid email format. Please enter a valid email address.")


def safe_text(prompt, field_name):
    """General text validation for names/categories that cannot be empty."""
    while True:
        value = input(prompt).strip()
        if not value:
            print(f"{field_name} cannot be empty.")
            continue

        if all(character.isalnum() or character in " -_" for character in value):
            return value

        print(f"Invalid {field_name.lower()}! Only letters, numbers, spaces, hyphens, and underscores are allowed.")


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
                email = safe_email("Email: ")
                service.add_member(name, email)

            elif choice == "2":
                service.list_members()

            elif choice == "3":
                m_id = safe_int("Member ID to update: ")
                new_name = safe_name("New Name: ")
                new_email = safe_email("New Email: ")
                service.update_member(m_id, new_name, new_email)

            elif choice == "4":
                name = safe_text("Equipment Name: ", "Equipment name")
                category = safe_text("Category: ", "Category")
                service.add_equipment(name, category)

            elif choice == "5":
                service.list_equipment()

            elif choice == "6":
                e_id = safe_int("Equipment ID to update: ")
                new_name = safe_text("New Equipment Name: ", "Equipment name")
                new_cat = safe_text("New Category: ", "Category")
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
