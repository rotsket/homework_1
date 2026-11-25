from typing import Union

import pytest
from src.Class_Marketplace import Product, Category

@pytest.fixture
def apple():
    return "apple", "it's very good apple", 100, 10

@pytest.fixture
def category_fruits():

    return "fruits", "Здесь находятся товары которые фрукты", None

def test_Product(apple):
    product = Product(*apple)

    assert product.name == "apple"
    assert product.description == "it's very good apple"
    assert product.price == 100
    assert product.quantity == 10

def test_Add_Category(category_fruits, apple):
    category = Category(*category_fruits)

    assert category.name == "fruits"
    assert category.description == "Здесь находятся товары которые фрукты"
    assert category.products == None


# def test_Add_Category(category_fruits, apple):
#     product_apple = Product(*apple)
#     category = Category(*category_fruits)
#     category.products = product_apple.name
#     assert category.name == "fruits"