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
        # Call self.load_data()
        self.load_data()

    def add_product(self, product):
        """Raises DuplicateProductError if ID exists."""
        # Check for duplicates, add, log.
        if product.product_id in self.products:
            raise DuplicateProductError(
                f"product with ID '{product.product_id}' already exists."
            )
        self.products[product.product_id] = product
        logger.info(f"Added product '{product.name}' (ID: {product.product_id}).")
        self.save_data()

    def remove_product(self, product_id):
        """Raises InvalidProductError if not found."""
        # Remove from dict, log.
        if product_id not in self.products:
            raise InvalidProductError(f"Product with ID '{product_id}' not found.")
        removed_product = self.products.pop(product_id)
        logger.info(
            f"Removed product '{removed_product.name}' (ID: {removed_product.product_id})."
        )
        self.save_data()

    def find_product(self, product_id):
        """Raises InvalidProductError if not found."""
        # Return product or raise.
        if product_id not in self.products:
            raise InvalidProductError(f"Product with ID '{product_id}' not found.")
        return self.products[product_id]

    def sell_product(self, product_id, qty):
        """Process a sale. Warn if stock drops below threshold."""
        # Find product, call sell(), check low stock.
        product = self.find_product(product_id)
        product.sell(qty)
        if (
            not isinstance(product, DigitalProduct)
            and product.quantity < self.low_stock_threshold
        ):
            logger.warning(
                f"Stock for '{product.name}' (ID: {product.product_id}) is low: {product.quantity} units remaining."
            )
        self.save_data()

    def restock_product(self, product_id, qty):
        # Find and restock.
        product = self.find_product(product_id)
        product.restock(qty)
        logger.info(
            f"Restocked {qty} units of '{product.name}' (ID: {product.product_id}). New stock: {product.quantity}."
        )
        self.save_data()

    def search(self, query):
        """Search by partial name or exact category."""
        # Use a list comprehension.
        query = query.lower()
        return [
            product
            for product in self.products.values()
            if query in product.name.lower() or query == product.category.lower()
        ]

    def low_stock_report(self):
        """Yield products below threshold (exclude digital). Lazy over large inventories."""
        for product in self.products.values():
            if (
                not isinstance(product, DigitalProduct)
                and product.quantity < self.low_stock_threshold
            ):
                yield product

    def stock_summary(self):
        """Return total quantity on hand by category (excludes digital)."""
        categories = {p.category for p in self.products.values()}
        return {
            category: sum(
                p.quantity
                for p in self.products.values()
                if p.category == category and not isinstance(p, DigitalProduct)
            )
            for category in categories
        }

    def stock_value_report(self):
        """Return total value (price * qty) by category."""
        categories = {p.category for p in self.products.values()}
        return {
            category: sum(
                p.price * p.quantity
                for p in self.products.values()
                if p.category == category and not isinstance(p, DigitalProduct)
            )
            for category in categories
        }

    def save_data(self):
        # Write product dicts to JSON.
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, "w") as f:
                json.dump(
                    [product.to_dict() for product in self.products.values()],
                    f,
                    indent=4,
                )
                logger.info(f"Inventory data saved to '{self.data_file}'.")
        except OSError as e:
            logger.error(f"Error saving inventory data to '{self.data_file}': {e}")

    def load_data(self):
        # Read JSON, use Product.from_dict() factory.
        self.products = {}
        if not os.path.exists(self.data_file):
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                raw = json.load(f)
            for item in raw:
                try:
                    product = Product.from_dict(item)
                    self.products[product.product_id] = product
                except (KeyError, TypeError, InvalidProductError) as e:
                    logger.warning(
                        f"Skipped corrupted product entry: {e} " f"Data: {item}"
                    )
            logger.info(f"Loaded {len(self.products)} products from {self.data_file} ")
        except json.JSONDecodeError as e:
            logger.error(f"Error loading inventory data from '{self.data_file}': {e}")
            self.products = {}
        except OSError as e:
            logger.error(f"Error accessing inventory data file '{self.data_file}': {e}")
            self.products = {}
