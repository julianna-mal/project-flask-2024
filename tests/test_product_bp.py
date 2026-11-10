import unittest
from run import app
from app.products.storage import add_product, delete_product


class ProductBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

        self.laptop_id = add_product({
            "name": "Laptop",
            "price": "1200",
            "content": "Потужний ноутбук",
            "category": "electronics",
            "quantity": 5,
            "image": None
        })

        self.phone_id = add_product({
            "name": "Phone",
            "price": "800",
            "content": "Смартфон",
            "category": "electronics",
            "quantity": 10,
            "image": None
        })

    def tearDown(self):
        delete_product(self.laptop_id)
        delete_product(self.phone_id)

    def test_products_list_page(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"Phone", response.data)

    def test_product_detail_page(self):
        response = self.client.get(
            f"/products/{self.laptop_id}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"1200", response.data)

    def test_product_not_found(self):
        response = self.client.get("/products/999999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
