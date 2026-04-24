# Project 4: Inventory Management System

## Team Members
- Olamide Adeboye
- Alex Omeje
- Kunle Fatade

## Description
A command-line inventory management system built in Python for small businesses to track products, manage stock levels, process sales, and generate on-demand reports. The system supports three product types (standard, perishable, and digital), persists data to JSON files between sessions, and maintains a full audit trail of every stock movement.

Built using object-oriented principles, the project demonstrates inheritance, polymorphism, encapsulation, and the factory method pattern. It uses only Python's standard library, so no external packages are required.

## How to Run
```bash
python main.py
```

On first run, the program automatically creates the `data/` and `logs/` folders. Use menu option 11 to save and exit safely.

## How to Run Tests
```bash
python -m unittest discover tests -v
```

## Features
- [x] Add products (standard, perishable, digital)
- [x] Sell and restock products with validation
- [x] Remove products by ID
- [x] Search by name (partial match) or category (exact match)
- [x] Low stock alerts with configurable threshold (default: 5 units)
- [x] Stock value report by category (price multiplied by quantity)
- [x] Stock summary report by category (total units on hand)
- [x] Transaction history log with timestamps
- [x] Data persistence (JSON auto-save after every change)
- [x] Logging to console (INFO level) and file (DEBUG level)
- [x] Custom exceptions (`OutOfStockError`, `InvalidProductError`, `DuplicateProductError`)
- [x] Test suite (26 tests across 4 test classes)

## Project Structure
```
.
├── main.py               # CLI entry point and menu loop
├── inventory.py          # Inventory manager class
├── products.py           # Product base class and     subclasses
├── transaction_log.py    # Stock movement audit trail
├── exceptions.py         # Custom exception types
├── data/
│   ├── inventory.json    # Persisted product data
│   └── log.json          # Persisted transaction history
├── logs/
│   └── inventory.log     # Application log file
└── tests/                # Unit tests
```

## Tech Stack
- **Language:** Python 3
- **Paradigm:** Object-Oriented Programming
- **Storage:** JSON files
- **Logging:** Python `logging` module
- **Testing:** Python `unittest` framework
- **External dependencies:** None

## Contribution Log
| Member | Contribution |
|--------|-------------|

| Olamide Adeboye | Project lead and architecture; transaction log module (`transaction_log.py`); data persistence layer; CLI menu (`main.py`); Git workflow and integration |test suite (26 tests across 4 test classes) |

| Alex Omeje | Core `Product` class and `PerishableProduct` / `DigitalProduct` subclasses (`products.py`)

| Kunle Fatade |core `Inventory` class (`inventory.py`); documentation