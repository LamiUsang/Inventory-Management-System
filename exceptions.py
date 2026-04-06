"""
Custom exceptions for the Inventory Management System.
"""


class OutOfStockError(Exception):
    """Raised when attempting to sell more units than available."""

    pass


class InvalidProductError(Exception):
    """Raised when product data is invalid."""

    pass


class DuplicateProductError(Exception):
    """Raised when a product with the same ID already exists."""

    pass
