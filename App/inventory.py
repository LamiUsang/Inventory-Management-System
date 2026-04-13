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
        self.products = {}  # TODO: Initialize empty product dictionary
        self.low_stock_threshold = low_stock_threshold  # TODO: Set low stock threshold
        self.data_file = data_file  # TODO: Store data file path
        self.load_data()  # TODO: Load products from JSON file

    def add_product(self, product):
        """Raises DuplicateProductError if ID exists."""
        # TODO: Check for duplicates and add product
        if product.product_id in self.products:
            raise DuplicateProductError(
                f"Product ID {product.product_id} already exists."
            )
        self.products[product.product_id] = product
        logger.info(f"Added product: {product.name}")

    def remove_product(self, product_id):
        """Raises InvalidProductError if not found."""
        # TODO: Remove product by ID
        if product_id not in self.products:
            raise InvalidProductError(f"Product ID {product_id} not found.")
        removed = self.products.pop(product_id)
        logger.info(f"Removed product: {removed.name}")

    def find_product(self, product_id):
        """Raises InvalidProductError if not found."""
        # TODO: Return product object or raise error
        if product_id not in self.products:
            raise InvalidProductError(f"Product ID {product_id} not found.")
        return self.products[product_id]

    def sell_product(self, product_id, qty):
        """Process a sale. Warn if stock drops below threshold."""
        # TODO: Find product, sell quantity, check low stock
        product = self.find_product(product_id)
        product.sell(qty)
        logger.info(f"Sold {qty} of {product.name}")
        if (
            not isinstance(product, DigitalProduct)
            and product.quantity < self.low_stock_threshold
        ):
            logger.warning(f"Low stock alert: {product.name} ({product.quantity} left)")

    def restock_product(self, product_id, qty):
        # TODO: Restock product by quantity
        product = self.find_product(product_id)
        product.restock(qty)
        logger.info(f"Restocked {qty} of {product.name}")

    def search(self, query):
        """Search by partial name or exact category."""
        # TODO: Use list comprehension to filter products
        q = query.lower()
        return [
            p
            for p in self.products.values()
            if q in p.name.lower() or q == p.category.lower()
        ]

    def low_stock_report(self):
        """Return products below threshold (exclude digital)."""
        # TODO: Use list comprehension to find low stock products
        return [
            p
            for p in self.products.values()
            if not isinstance(p, DigitalProduct)
            and p.quantity < self.low_stock_threshold
        ]

    def category_summary(self):
        """Return total quantity of products per category."""
        # TODO: Use dict comprehension to aggregate by category
        return {
            cat: sum(p.quantity for p in self.products.values() if p.category == cat)
            for cat in {p.category for p in self.products.values()}
        }

    def stock_value_report(self):
        """Return total value (price * quantity) per category."""
        # TODO: Use dict comprehension to calculate total value per category
        return {
            cat: sum(
                p.price * p.quantity
                for p in self.products.values()
                if p.category == cat
            )
            for cat in {p.category for p in self.products.values()}
        }

    def save_data(self):
        # TODO: Write all product dicts to JSON
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        data = [p.to_dict() for p in self.products.values()]
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=4)
        logger.info("Inventory data saved.")

    def load_data(self):
        # TODO: Load JSON data and recreate Product objects
        if not os.path.exists(self.data_file):
            logger.warning("Data file not found. Starting with empty inventory.")
            return
        with open(self.data_file, "r") as f:
            data = json.load(f)
        for item in data:
            product = Product.from_dict(item)
            self.products[product.product_id] = product
        logger.info("Inventory data loaded.")
