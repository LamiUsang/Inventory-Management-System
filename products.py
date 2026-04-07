"""
Product classes for the Inventory Management System.
Base class and subclasses: PerishableProduct, DigitalProduct.
"""

import logging
from datetime import datetime
from exceptions import OutOfStockError, InvalidProductError

logger = logging.getLogger("InventoryManager")


class Product:
       def __init__(self, product_id, name, price, quantity, category):
           self.product_id = product_id
           self.name = name
           self.price = price
           self.quantity = quantity
           self.category = category
           
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
     def __init__(self, product_id, name, price, quantity, category, expiry_date):
        super().__init__(product_id, name, price, quantity, category)
         self.expiry_date = expiry date

product_im001 = PerishableProduct(
    product_id="IM001",
    name="Milk",
    price=16.55,
    quantity=200,
    category="Dairy",
    shelf_life="3 months"
)

product_im002 = PerishableProduct(
    product_id="IM002",
    name="Bread",
    price=2.99,
    quantity=100,
    category="Gluten Free",
    shelf_life="2 weeks"
)

product_im003 = PerishableProduct(
    product_id="IM003",
    name="Sugar",
    price=1.20,
    quantity=200,
    category="Confectionary",
    shelf_life="6 months"
)

product_im004 = PerishableProduct(
    product_id="IM004",
    name="Egg",
    price=6.5,
    quantity=50,
    category="Free Range",
    shelf_life="2 Weeks"
)

product_im005 = PerishableProduct(
    product_id="IM005",
    name="Butter",
    price=5.0,
    quantity=100,
    category="Plant Based",
    shelf_life="6 months"
)
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
     def __init__(self, product_id, name, price, category, download_link):
        super().__init__(product_id, name, price, 0, category)
product_im006 = DigitalProduct(
    product_id="IM006",
    name="Python ebook",
    price=5.99,
    quantity=0
    category="ebook",
    download_link="download_link"
)

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
