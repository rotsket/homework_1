class Product:
    name = str
    description = str
    price = float | int
    quantity = int
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

class Category:
    name = str
    description = str
    products = list | None

    categories_count : int = 0
    product_count : int = 0
    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.products = products if products else []

        Category.categories_count += 1
        Category.product_count += len(self.products) if self.products else 0


