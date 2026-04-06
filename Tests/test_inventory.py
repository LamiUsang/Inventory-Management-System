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
        pass
    def test_negative_price_raises(self):
        pass
    def test_sell_reduces_stock(self):
        pass
    def test_sell_exceeds_stock_raises(self):
        pass
    def test_restock_increases_stock(self):
        pass
    def test_to_dict_and_from_dict(self):
        pass

class TestPerishableProduct(unittest.TestCase):
    def test_expired_product(self):
        pass
    def test_sell_expired_raises(self):
        pass

class TestDigitalProduct(unittest.TestCase):
    def test_sell_returns_download_link(self):
        pass
    def test_sell_does_not_change_quantity(self):
        pass

class TestInventory(unittest.TestCase):
    def test_add_product(self):
        pass
    def test_add_duplicate_raises(self):
        pass
    def test_search_by_name(self):
        pass
    def test_low_stock_report(self):
        pass
    def test_stock_value_report(self):
        pass
    def test_save_and_load(self):
        pass

class TestTransactionLog(unittest.TestCase):
    def test_record_entry(self):
        pass
    def test_save_and_load(self):
        pass


if __name__ == "__main__":
    unittest.main()
