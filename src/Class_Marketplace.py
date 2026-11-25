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
    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.products = products if products else None


