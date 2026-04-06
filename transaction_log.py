"""
TransactionLog class for the Inventory Management System.
"""

import json
import logging
import os
from datetime import datetime

logger = logging.getLogger("InventoryManager")


class TransactionLog:
    """Records all stock movements with timestamps."""

    def __init__(self, log_file="data/log.json"):
        self.entries = []
        self.log_file = log_file
        self.load()

    def record(self, action, product_id, product_name, qty, details=""):
        """Record a stock movement with timestamp."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "product_id": product_id,
            "product_name": product_name,
            "quantity": qty,
            "details": details,
        }
        self.entries.append(entry)
        # add to list
        logger.info(
            f"{action} - {product_name} (ID: {product_id}), Qty: ({qty})"
        )  # optional log
        self.save()  # Save after each transaction

    def summary(self, product_id=None):
        """Display transaction history. Filter by product_id if given."""
        if product_id is not None:
            filtered = [e for e in self.entries if e["product_id"] == product_id]
        else:
            filtered = self.entries
        for e in filtered:
            print(
                f"{e['timestamp']} - {e['action']} - {e['product_name']} - Qty: {e['quantity']}"
            )

    def save(self):
        # Write entries to JSON.
        try:
            with open(self.log_file, "w") as file:
                json.dump(self.entries, file, indent=4)
        except Exception as e:
            print(f"Error saving transaction log: {e}")

    def load(self):
        # TODO: Read from JSON, handle missing file.
        try:
            with open(self.log_file, "r") as file:
                self.entries = json.load(file)

        except FileNotFoundError:
            print(f"Log file not found: {self.log_file}")
        except Exception as e:
            print(f"Error loading transactions: {e}")
            self.entries = []
