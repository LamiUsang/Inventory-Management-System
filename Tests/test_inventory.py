"""
Test Suite for Project 4: Inventory Management System
Run with: python -m unittest tests/test_inventory.py -v
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from products import Product, PerishableProduct, DigitalProduct
from inventory import Inventory
from transaction_log import TransactionLog
from exceptions import OutOfStockError, InvalidProductError, DuplicateProductError


class TestProduct(unittest.TestCase):
    def test_create_valid_product(self):
        # A product created with valid fields stores all attributes correctly.
        p = Product("P001", "Rice", 1.99, 50, "Staple food")
        self.assertEqual(p.product_id, "P001")
        self.assertEqual(p.name, "Rice")
        self.assertEqual(p.price, 1.99)
        self.assertEqual(p.quantity, 50)
        self.assertEqual(p.category, "Staple food")

    def test_negative_price_raises(self):
        # A negative price sshould raise InvalidProductError
        with self.assertRaises(InvalidProductError):
            Product("P002", "Beans", -0.99, 30, "Staple Food")

    def test_zero_prce_raises(self):
        # A zero price should raise InvalidProductError
        with self.assertRaises(InvalidProductError):
            Product("P003", "Lentils", 0, 20, "Staple Food")

    def test_sell_reduces_stock(self):
        # Selling reduces quantity by the correct amount.
        p = Product("P004", "Sugar", 0.99, 100, "Staple Food")
        p.sell(10)
        self.assertEqual(p.quantity, 90)

    def test_sell_exceeds_stock_raises(self):
        # Selling more than available stock raises OutOfStockError
        p = Product("P005", "Salt", 0.49, 20, "Condiment")
        with self.assertRaises(OutOfStockError):
            p.sell(25)

    def test_restock_increases_stock(self):
        # Restocking increases quantity by the correct amount.
        p = Product("P006", "Flour", 2.49, 40, "Baking")
        p.restock(20)
        self.assertEqual(p.quantity, 60)

    def test_to_dict_and_from_dict(self):
        # A product converted to a dictionary and back retains all attributes correctly.
        p = Product("P007", "Yeast", 0.79, 15, "Baking")
        data = p.to_dict()
        restored = Product.from_dict(data)
        self.assertEqual(restored.product_id, p.product_id)
        self.assertEqual(restored.name, p.name)
        self.assertEqual(restored.price, p.price)
        self.assertEqual(restored.quantity, p.quantity)
        self.assertEqual(restored.category, p.category)


class TestPerishableProduct(unittest.TestCase):
    def test_expired_product(self):
        # A product with a past expir date should report as expired.
        p = PerishableProduct("P008", "Milk", 2.99, 10, "Dairy", "2024-01-01")
        self.assertTrue(p.is_expired())

    def test_valid_product_not_expired(self):
        # A product with a future expiry date should not report as expired.
        p = PerishableProduct("P009", "Cheese", 3.99, 5, "Dairy", "2026-12-31")
        self.assertFalse(p.is_expired())

    def test_sell_expired_raises(self):
        # Selling an expired Product should raise InvalidProductError.
        p = PerishableProduct("P010", "Yogurt", 1.49, 20, "Dairy", "2024-01-01")
        with self.assertRaises(OutOfStockError):
            p.sell(5)

    def test_invalid_expiry_format_raises(self):
        # Creating a PerishableProduct with an invalid expiry date format should raise InvalidProductError.
        with self.assertRaises(InvalidProductError):
            PerishableProduct("P011", "Butter", 2.49, 10, "Dairy", "01-01-2024")


class TestDigitalProduct(unittest.TestCase):
    def test_sell_returns_download_link(self):
        # Selling a Digital Product should return the download link.
        p = DigitalProduct(
            "P012", "Skill Traverse Ebook", 9.99, "Books", "http://example.com/download"
        )
        link = p.sell()
        self.assertEqual(link, "http://example.com/download")

    def test_sell_does_not_change_quantity(self):
        # Selling a Digital Product should not change the quantity.
        p = DigitalProduct(
            "P013", "Python Course", 49.99, "Courses", "http://example.com/python"
        )
        p.sell()
        self.assertEqual(p.quantity, 0)

    def test_empty_download_link_raises(self):
        # Creating a Digital Product with an empty download link should raise InvalidProductError.
        with self.assertRaises(InvalidProductError):
            DigitalProduct("P014", "Empty Link Product", 19.99, "Misc", "")


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.test_file = "tests/test_inventory.json"
        self.inventory = Inventory(self.test_file, low_stock_threshold=5)
        self.inventory.products = {}

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_product(self):
        # Adding a product to the inventory should store it correctly.
        product = Product("P015", "onions", 1.99, 10, "Staple Food")
        self.inventory.add_product(product)
        self.assertIn("P015", self.inventory.products)

    def test_add_duplicate_raises(self):
        # Adding a product with an existing product_id should raise DuplicateProductError.
        product = Product("P015", "onions", 1.99, 10, "Staple Food")
        self.inventory.add_product(product)
        with self.assertRaises(DuplicateProductError):
            self.inventory.add_product(product)

    def test_remove_product(self):
        # Removing a product should mean it can no longer be found.
        product = Product("P016", "Garlic", 0.99, 15, "Staple Food")
        self.inventory.add_product(product)
        self.inventory.remove_product("P016")
        self.assertNotIn("P016", self.inventory.products)

    def test_search_by_name(self):
        # Partial name search should return matching products.
        product1 = Product("P017", "Tomatoes", 2.49, 20, "Vegetables")
        product2 = Product("P018", "Cherry Tomatoes", 3.49, 10, "Vegetables")
        self.inventory.add_product(product1)
        self.inventory.add_product(product2)

        results = self.inventory.search("Tom")
        self.assertEqual(len(results), 2)

    def test_search_by_category(self):
        # Exact category search should return matching products.
        product = Product("P019", "Cucumbers", 1.49, 25, "Vegetables")
        self.inventory.add_product(product)
        results = self.inventory.search("Vegetables")
        self.assertEqual(len(results), 1)

    def test_low_stock_report(self):
        # only products below the low stock threshold should be included in the low stock report.
        product = Product("P020", "Lettuce", 0.99, 3, "Vegetables")
        self.inventory.add_product(product)
        low_stock_report = list(self.inventory.low_stock_report())
        self.assertEqual(len(low_stock_report), 1)
        self.assertEqual(low_stock_report[0].product_id, "P020")

    def test_low_stock_report_excludes_digital(self):
        # Digital products should not be included in the low stock report, even if they have a quantity of 0.
        product = DigitalProduct(
            "P021", "Ebook", 9.99, "Books", "http://example.com/ebook"
        )
        self.inventory.add_product(product)
        low_stock_report = list(self.inventory.low_stock_report())
        self.assertEqual(len(low_stock_report), 0)

    def test_stock_value_report(self):
        # The stock value per category should be price times quantity.
        product1 = Product("P022", "Bread", 2.99, 10, "Bakery")
        product2 = Product("P023", "Cake", 15.99, 5, "Bakery")
        self.inventory.add_product(product1)
        self.inventory.add_product(product2)
        stock_value_report = self.inventory.stock_value_report()
        self.assertAlmostEqual(
            stock_value_report["Bakery"], 2.99 * 10 + 15.99 * 5, places=2
        )

    def test_stock_summary(self):
        # Stock summary returns total quantity on hand per category.
        product1 = Product("P024", "Apples", 0.50, 12, "Produce")
        product2 = Product("P025", "Pears", 0.80, 8, "Produce")
        self.inventory.add_product(product1)
        self.inventory.add_product(product2)
        summary = self.inventory.stock_summary()
        self.assertEqual(summary["Produce"], 20)

    def test_save_and_load(self):
        # Products saved to a file should be loaded with the same attributes intact.
        product = Product("P026", "Eggs", 3.49, 12, "Dairy")
        self.inventory.add_product(product)
        self.inventory.save_data()
        new_inventory = Inventory(self.test_file, low_stock_threshold=5)
        self.assertIn("P026", new_inventory.products)
        self.assertEqual(new_inventory.products["P026"].name, "Eggs")


class TestTransactionLog(unittest.TestCase):
    def setUp(self):
        self.test_file = "tests/test_log.json"
        self.log = TransactionLog(log_file=self.test_file)
        self.log.entries = []

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_record_entry(self):
        # Recording a transaction should store all details correctly.
        self.log.record("sell", "P027", "Butter", 2)
        self.assertEqual(len(self.log.entries), 1)
        entry = self.log.entries[0]
        self.assertEqual(entry["action"], "sell")
        self.assertEqual(entry["product_id"], "P027")
        self.assertEqual(entry["product_name"], "Butter")
        self.assertEqual(entry["quantity"], 2)

    def test_save_and_load(self):
        # Transactions saved to a file should be loaded with the same details intact.
        self.log.record("restock", "P028", "Jam", 5)
        self.log.save()
        new_log = TransactionLog(log_file=self.test_file)
        self.assertEqual(len(new_log.entries), 1)
        entry = new_log.entries[0]
        self.assertEqual(entry["action"], "restock")
        self.assertEqual(entry["product_id"], "P028")
        self.assertEqual(entry["product_name"], "Jam")
        self.assertEqual(entry["quantity"], 5)


if __name__ == "__main__":
    unittest.main()
