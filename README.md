# Campus MakerSpace Checkout System

An Object-Oriented CLI application written in Python and backed by SQLite to manage campus makerspace member registration, equipment inventory, and checkouts.

## How to Run

1. Clone the repository:
   git clone https://github.com/Frank-1mbuki/Lab_Makerspace_Frank-1mbuki.git
   cd Lab_Makerspace_Frank-1mbuki

2. Run the application:
   python main.py

## Project Structure

- main.py: Entry point for the CLI menu loop.
- models.py: Domain classes (Member, Equipment, Loan).
- database.py: SQLite connection setup and table initialization.
- services.py: Business operations and database queries.
- requirements.txt: Dependency list (uses standard library).