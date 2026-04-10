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
        # Validate string fields
        if not isinstance(product_id, str) or not product_id.strip():
            raise InvalidProductError("Product ID must be a non-empty string.")
        if not isinstance(name, str) or not name.strip():
            raise InvalidProductError("Product name must be a non-empty string.")
        if not isinstance(category, str) or not category.strip():
            raise InvalidProductError("Product category must be a non-empty string.")
        # Validate Price
        if not isinstance(price, (int, float)) or price <= 0:
            raise InvalidProductError("Price must be a positive number.")
        # Validate Quantity
        if not isinstance(quantity, int) or quantity < 0:
            raise InvalidProductError("Quantity must be a non-negative integer.")
        # Assign all attributes.
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category

    def sell(self, qty):
        """
        Reduce stock by qty.

        Raises:
            OutOfStockError: If qty exceeds available stock.
        """
        # Validate qty > 0, check stock, reduce, log.
        if not isinstance(qty, int) or qty <= 0:
            raise InvalidProductError("Quantity to sell must be a positive integer.")
        if qty > self.quantity:
            raise OutOfStockError(
                f"Not enough stock for {self.name}. Available stock: {self.quantity}, requested: {qty}."
            )
        self.quantity -= qty
        logger.info(
            f"sold {qty} units of '{self.name}' (ID: {self.product_id}). Remaining stock: {self.quantity}."
        )

    def restock(self, qty):
        """Increase stock by qty."""
        # Validate qty > 0, increase, log.
        if not isinstance(qty, int) or qty <= 0:
            raise InvalidProductError("Quantity to restock must be a positive integer.")
        self.quantity += qty
        logger.info(
            f"restocked {qty} units of '{self.name}' (ID: {self.product_id}). New stock: {self.quantity}."
        )

    def __str__(self):
        # Formatted string with all product details.
        return (
            f"Product:: {self.name} | "
            f"ID: {self.product_id} | "
            f"Price: £{self.price:.2f} | "
            f"Quantity: {self.quantity} |"
            f"Category: {self.category} | "
        )

    def to_dict(self):
        # Return dict with all attributes plus "type": "standard".
        return {
            "type": "standard",
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "category": self.category,
        }

    @classmethod
    def from_dict(cls, data):
        """Factory method: create correct subclass from a dict."""
        # Check data["type"] and return correct subclass.
        product_type = data.get("type: standard")
        if product_type == "perishable":
            return PerishableProduct(
                product_id=data["product_id"],
                name=data["name"],
                price=data["price"],
                quantity=data["quantity"],
                category=data["category"],
                expiry_date=data["expiry_date"],
            )
        elif product_type == "digital":
            return DigitalProduct(
                product_id=data["product_id"],
                name=data["name"],
                price=data["price"],
                category=data["category"],
                download_link=data["download_link"],
            )
        else:
            return cls(
                product_id=data["product_id"],
                name=data["name"],
                price=data["price"],
                quantity=data["quantity"],
                category=data["category"],
            )


class PerishableProduct(Product):
    """A product with an expiry date."""

    def __init__(self, product_id, name, price, quantity, category, expiry_date):
        super().__init__(product_id, name, price, quantity, category)
        # Validate expiry_date format (YYYY-MM-DD).
        if not isinstance(expiry_date, str) or not expiry_date.strip():
            raise InvalidProductError(
                "Expiry date must be a non-empty string in YYYY-MM-DD format."
            )
        try:
            datetime.strptime(expiry_date, "%Y-%m-%d")
        except ValueError:
            raise InvalidProductError("Expiry date must be in YYYY-MM-DD format.")
        # Assign self.expiry_date.
        self.expiry_date = expiry_date.strip()

    def is_expired(self):
        """Return True if past expiry date."""
        # Compare to today's date.
        expiry = datetime.strptime(self.expiry_date, "%Y-%m-%d").date()
        today = datetime.today().date()
        return expiry < today

    def sell(self, qty):
        """Check expiry before selling."""
        # If expired, raise OutOfStockError.
        if self.is_expired():
            raise OutOfStockError(
                f"Cannot sell '{self.name}' (ID: {self.product_id}) because it is expired (expiry date: {self.expiry_date})."
            )
        # Otherwise call super().sell(qty).
        super().sell(qty)

    def to_dict(self):
        # Add expiry_date and "type": "perishable".
        data = super().to_dict()
        data["type"] = "perishable"
        data["expiry_date"] = self.expiry_date
        return data


class DigitalProduct(Product):
    """A digital product with a download link (unlimited supply)."""

    def __init__(self, product_id, name, price, category, download_link):
        super().__init__(product_id, name, price, 0, category)
        # Validate download_link non-empty.
        if not isinstance(download_link, str) or not download_link.strip():
            raise InvalidProductError("Download link must be a non-empty string.")
        self.download_link = download_link.strip()

    def sell(self, qty=1):
        """No stock decrement. Log and return download link."""
        # Log sale, return self.download_link.
        logger.info(
            f"sold {qty} units of digital product '{self.name}' (ID: {self.product_id}). Download link: {self.download_link}."
        )
        return self.download_link

    def get_download_link(self):
        return self.download_link

    def to_dict(self):
        # Add download_link and "type": "digital".
        data = super().to_dict()
        data["type"] = "digital"
        data["download_link"] = self.download_link
        return data
