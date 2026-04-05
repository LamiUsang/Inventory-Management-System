class Product:
    def __init__(
        self,
        product_id,
        name,
        unit_quantity,
        unit_price,
        stock,
        category,
        shelf_life=None,
    ):
        self.product_id = product_id
        self.name = name
        self.unit_quantity = unit_quantity
        self.unit_price = unit_price
        self.stock = stock
        self.category = category
        self.shelf_life = shelf_life

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "unit_quantity": self.unit_quantity,
            "unit_price": self.unit_price,
            "stock": self.stock,
            "category": self.category,
            "shelf_life": self.shelf_life,
        }


class Inventory:
    def __init__(self):
        self.products = {}  # store products using product_id as key

    # Add product (initial stocking)
    def add_product(self, product):
        self.products[product.product_id] = product

    # Remove product (sales, expired, theft etc.)
    def remove_product(self, product_id, quantity):
        if product_id in self.products:
            product = self.products[product_id]
            if product.stock >= quantity:
                product.stock -= quantity
            else:
                print("Not enough stock to remove.")
        else:
            print("Product not found.")

    # Restock product
    def restock_product(self, product_id, quantity):
        if product_id in self.products:
            self.products[product_id].stock += quantity
        else:
            print("Product not found.")

    # Sell product (same as remove but semantic clarity)
    def sell_product(self, product_id, quantity):
        self.remove_product(product_id, quantity)

    # Search product by name or ID
    def search_product(self, keyword):
        results = [
            p.to_dict()
            for p in self.products.values()
            if keyword.lower() in p.name.lower()
            or keyword.lower() in p.product_id.lower()
        ]
        return results

    # Low stock generator
    def low_stock(self, threshold=50):
        return [p.to_dict() for p in self.products.values() if p.stock <= threshold]

    # Category summary using dict comprehension
    def category_summary(self):
        return {
            category: sum(
                p.stock for p in self.products.values() if p.category == category
            )
            for category in set(p.category for p in self.products.values())
        }

    # Inventory value report (price * stock)
    def value_report(self):
        return {
            p.product_id: {"name": p.name, "total_value": p.unit_price * p.stock}
            for p in self.products.values()
        }


# ------------------ Example Usage ------------------

inventory = Inventory()

inventory.add_product(
    Product("IM001", "Milk", "1 Tin", 16.55, 200, "Dairy", "3 months")
)
inventory.add_product(
    Product("IM002", "Bread", "1 loaf", 2.99, 100, "Gluten Free", "2 weeks")
)
inventory.add_product(
    Product("IM003", "Sugar", "1 Pack", 1.20, 200, "Confectionery", "6 months")
)
inventory.add_product(
    Product("IM004", "Eggs", "1 Crate", 6.50, 50, "Free Range", "2 weeks")
)
inventory.add_product(
    Product("IM005", "Butter", "1 Pack", 5.00, 100, "Plant based", "6 months")
)
inventory.add_product(Product("IM006", "Python Ebook", "1", 5.99, 999, "ebook"))

# Example operations
inventory.sell_product("IM001", 10)
inventory.restock_product("IM004", 20)

print("Search:", inventory.search_product("Milk"))
print("Low Stock:", inventory.low_stock(60))
print("Category Summary:", inventory.category_summary())
print("Value Report:", inventory.value_report())
