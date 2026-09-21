from database import init_db
from services import MakerSpaceService

def main():
    init_db()
    service = MakerSpaceService()

    while True:
        print("\n1. Add Member\n2. Checkout Item\n0. Exit")
        choice = input("Option: ")

        if choice == "1":
            service.add_member(input("Name: "), input("Email: "))
        elif choice == "2":
            service.checkout_equipment(int(input("Member ID: ")), int(input("Item ID: ")))
        elif choice == "0":
            break

if __name__ == "__main__":
    main()