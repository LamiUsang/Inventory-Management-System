"""
Project 4: Inventory Management System
Entry point. Run with: python main.py
"""

import logging
import os

from products import Product, PerishableProduct, DigitalProduct
from inventory import Inventory
from transaction_log import TransactionLog
from exceptions import OutOfStockError, InvalidProductError, DuplicateProductError

# TODO: Configure logging (console INFO + file DEBUG)
logger = logging.getLogger("InventoryManager")


def display_menu():
    print("\n" + "=" * 50)
    print("   Inventory Management System")
    print("=" * 50)
    print("1.  Add a new product")
    print("2.  View all products")
    print("3.  Search products")
    print("4.  Sell a product")
    print("5.  Restock a product")
    print("6.  Remove a product")
    print("7.  Low stock report")
    print("8.  Stock value report")
    print("9.  Transaction history")
    print("10. Save and exit")
    print("=" * 50)


def main():
    inventory = Inventory()
    log = TransactionLog()

    while True:
        display_menu()
        choice = input("\nEnter your choice (1-10): ").strip()

        if choice == "1":
            # TODO: Prompt for product type, fields, create and add.
            pass
        elif choice == "2":
            # TODO: Display all products.
            pass
        elif choice == "3":
            # TODO: Search and display.
            pass
        elif choice == "4":
            # TODO: Sell product, log transaction.
            pass
        elif choice == "5":
            # TODO: Restock product, log transaction.
            pass
        elif choice == "6":
            # TODO: Remove product, log transaction.
            pass
        elif choice == "7":
            # TODO: Low stock report.
            pass
        elif choice == "8":
            # TODO: Stock value report.
            pass
        elif choice == "9":
            # TODO: Transaction history.
            pass
        elif choice == "10":
            inventory.save_data()
            log.save()
            print("\nData saved. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 10.")


if __name__ == "__main__":
    main()
