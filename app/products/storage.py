import os
from tinydb import TinyDB, Query
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "products.json")

db = TinyDB(DB_PATH)
products_table = db.table("products")


def get_all_products():
    return products_table.all()


def get_product(product_id):
    Product = Query()
    return products_table.get(Product.id == product_id)


def add_product(data):
    Product = Query()

    existing_ids = [
        product["id"] for product in products_table.all()
    ]

    new_id = max(existing_ids, default=0) + 1

    data["id"] = new_id
    data["created_at"] = datetime.now().isoformat()

    products_table.insert(data)

    return new_id


def update_product(product_id, data):
    Product = Query()

    products_table.update(
        data,
        Product.id == product_id
    )


def delete_product(product_id):
    Product = Query()

    products_table.remove(
        Product.id == product_id
    )