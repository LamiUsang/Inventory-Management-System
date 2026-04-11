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

# Configure logging (console INFO + file DEBUG)
os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("InventoryManager")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler("logs/inventory.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


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

        try:
            if choice == "1":
                print("\nSelect product type:")
                print("1. Standard Product")
                print("2. Perishable Product")
                print("3. Digital Product")

                product_type = input("Enter product type: ").strip()
                product_id = input("Enter product ID: ").strip()
                name = input("Enter product name: ").strip()
                price = float(input("Enter price: ").strip())
                category = input("Enter category: ").strip()

                if product_type == "1":
                    quantity = int(input("Enter quantity: ").strip())
                    product = Product(product_id, name, price, quantity, category)

                elif product_type == "2":
                    quantity = int(input("Enter quantity: ").strip())
                    expiry_date = input("Enter expiry date (YYYY-MM-DD): ").strip()
                    product = PerishableProduct(
                        product_id, name, price, quantity, category, expiry_date
                    )

                elif product_type == "3":
                    download_link = input("Enter download link: ").strip()
                    product = DigitalProduct(
                        product_id, name, price, category, download_link
                    )

                else:
                    print("\nInvalid product type.")
                    continue

                inventory.add_product(product)
                log.record(
                    "add",
                    product.product_id,
                    product.name,
                    product.quantity,
                    "Product added",
                )
                print("\nProduct added successfully.")

            elif choice == "2":
                if not inventory.products:
                    print("\nNo products in inventory.")
                else:
                    print("\nAll Products:")
                    for product in inventory.products.values():
                        print(product)

            elif choice == "3":
                query = input("\nEnter product name or category to search: ").strip()
                results = inventory.search(query)

                if not results:
                    print("\nNo matching products found.")
                else:
                    print("\nSearch Results:")
                    for product in results:
                        print(product)

            elif choice == "4":
                product_id = input("\nEnter product ID to sell: ").strip()
                qty = int(input("Enter quantity to sell: ").strip())

                product = inventory.find_product(product_id)
                inventory.sell_product(product_id, qty)

                log.record(
                    "sale", product.product_id, product.name, qty, "Product sold"
                )
                print("\nSale completed successfully.")

            elif choice == "5":
                product_id = input("\nEnter product ID to restock: ").strip()
                qty = int(input("Enter quantity to restock: ").strip())

                product = inventory.find_product(product_id)
                inventory.restock_product(product_id, qty)

                log.record(
                    "restock",
                    product.product_id,
                    product.name,
                    qty,
                    "Product restocked",
                )
                print("\nProduct restocked successfully.")

            elif choice == "6":
                product_id = input("\nEnter product ID to remove: ").strip()
                product = inventory.find_product(product_id)

                inventory.remove_product(product_id)
                log.record(
                    "remove",
                    product.product_id,
                    product.name,
                    product.quantity,
                    "Product removed",
                )
                print("\nProduct removed successfully.")

            elif choice == "7":
                low_stock_products = inventory.low_stock_report()

                if not low_stock_products:
                    print("\nNo low-stock products.")
                else:
                    print("\nLow Stock Report:")
                    for product in low_stock_products:
                        print(product)

            elif choice == "8":
                report = inventory.stock_value_report()

                if not report:
                    print("\nNo stock value data available.")
                else:
                    print("\nStock Value Report:")
                    for category, value in report.items():
                        print(f"{category}: {value:.2f}")
            elif choice == "9":
                print("\nTransaction History:")
                log.summary()

            elif choice == "10":
                inventory.save_data()
                log.save()
                print("\nData saved. Goodbye!")
                break

            else:
                print("\nInvalid choice. Please enter a number between 1 and 10.")

        except ValueError:
            print("\nInvalid input. Please enter the correct data type.")
        except DuplicateProductError as e:
            print(f"\nError: {e}")
        except InvalidProductError as e:
            print(f"\nError: {e}")
        except OutOfStockError as e:
            print(f"\nError: {e}")
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            logger.exception("Unexpected error occurred")


if __name__ == "__main__":
    main()
