"""
Inventory class for the Inventory Management System.
"""

import json
import logging
import os

from products import Product, PerishableProduct, DigitalProduct
from exceptions import DuplicateProductError, InvalidProductError

logger = logging.getLogger("InventoryManager")


class Inventory:
    """Manages a collection of products."""

    def __init__(self, data_file="data/inventory.json", low_stock_threshold=5):
        self.products = {}
        self.low_stock_threshold = low_stock_threshold
        self.data_file = data_file
        # TODO: Call self.load_data()

    def add_product(self, product):
        """Raises DuplicateProductError if ID exists."""
        # TODO: Check for duplicates, add, log.
        pass

    def remove_product(self, product_id):
        """Raises InvalidProductError if not found."""
        # TODO: Remove from dict, log.
        pass

    def find_product(self, product_id):
        """Raises InvalidProductError if not found."""
        # TODO: Return product or raise.
        pass

    def sell_product(self, product_id, qty):
        """Process a sale. Warn if stock drops below threshold."""
        # TODO: Find product, call sell(), check low stock.
        pass

    def restock_product(self, product_id, qty):
        # TODO: Find and restock.
        pass

    def search(self, query):
        """Search by partial name or exact category."""
        # TODO: Use a list comprehension.
        pass

    def low_stock_report(self):
        """Return products below threshold (exclude digital)."""
        # TODO: Use a list comprehension to filter.
        pass

    def stock_value_report(self):
        """Return total value (price * qty) by category."""
        # TODO: Use a loop or dict comprehension.
        pass

    def save_data(self):
        # TODO: Write product dicts to JSON.
        pass

    def load_data(self):
        # TODO: Read JSON, use Product.from_dict() factory.
        pass
