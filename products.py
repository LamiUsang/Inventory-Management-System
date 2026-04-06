"""
Product classes for the Inventory Management System.
Base class and subclasses: PerishableProduct, DigitalProduct.
"""

import logging
from datetime import datetime
from exceptions import OutOfStockError, InvalidProductError

logger = logging.getLogger("InventoryManager")


class Product:
    """Base class for all products."""

    def __init__(self, product_id, name, price, quantity, category):
        """
        Raises:
            InvalidProductError: If any validation fails.
        """
        # TODO: Validate all fields:
        #   - product_id, name, category: non-empty strings
        #   - price: positive number
        #   - quantity: non-negative integer
        # TODO: Assign all attributes.
        pass

    def sell(self, qty):
        """
        Reduce stock by qty.

        Raises:
            OutOfStockError: If qty exceeds available stock.
        """
        # TODO: Validate qty > 0, check stock, reduce, log.
        pass

    def restock(self, qty):
        """Increase stock by qty."""
        # TODO: Validate qty > 0, increase, log.
        pass

    def __str__(self):
        # TODO: Formatted string with all product details.
        pass

    def to_dict(self):
        # TODO: Return dict with all attributes plus "type": "standard".
        pass

    @classmethod
    def from_dict(cls, data):
        """Factory method: create correct subclass from a dict."""
        # TODO: Check data["type"] and return correct subclass.
        pass


class PerishableProduct(Product):
    """A product with an expiry date."""

    def __init__(self, product_id, name, price, quantity, category, expiry_date):
        super().__init__(product_id, name, price, quantity, category)
        # TODO: Validate expiry_date format (YYYY-MM-DD).
        # TODO: Assign self.expiry_date.
        pass

    def is_expired(self):
        """Return True if past expiry date."""
        # TODO: Compare to today's date.
        pass

    def sell(self, qty):
        """Check expiry before selling."""
        # TODO: If expired, raise OutOfStockError.
        # TODO: Otherwise call super().sell(qty).
        pass

    def to_dict(self):
        # TODO: Add expiry_date and "type": "perishable".
        pass


class DigitalProduct(Product):
    """A digital product with a download link (unlimited supply)."""

    def __init__(self, product_id, name, price, category, download_link):
        super().__init__(product_id, name, price, 0, category)
        # TODO: Validate download_link non-empty.
        pass

    def sell(self, qty=1):
        """No stock decrement. Log and return download link."""
        # TODO: Log sale, return self.download_link.
        pass

    def get_download_link(self):
        return self.download_link

    def to_dict(self):
        # TODO: Add download_link and "type": "digital".
        pass
