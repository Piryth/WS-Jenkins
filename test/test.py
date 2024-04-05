import json
import unittest
import uuid

import requests


class MyTestCase(unittest.TestCase):

    def test_titles_insert(self):
        url = "http://localhost:5000/products?secret=loremipsumdolorsitamet"

        payload = json.dumps({
            "id": uuid.uuid4().__str__(),
            "title": "food",
            "cost": 15
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Product inserted")

    def test_titles_insert_no_secret(self):
        url = "http://localhost:5000/products?secret="
        id = "myid"
        payload = json.dumps({
            "id": id,
            "title": "test_insert_no_secret",
            "cost": 15
        })
        headers = {
            'Content-Type': 'application/json'
        }

        # First product inserted
        response = requests.request("POST", url, headers=headers, data=payload)
        self.assertEqual(response.status_code, 403)

    def test_titles_insert_conflict(self):
        url = "http://localhost:5000/products?secret=loremipsumdolorsitamet"
        id = uuid.uuid4().__str__()
        payload = json.dumps({
            "id": id,
            "title": "test_insert_no_secret",
            "cost": 15
        })
        headers = {
            'Content-Type': 'application/json'
        }

        # First product inserted
        response = requests.request("POST", url, headers=headers, data=payload)
        self.assertEqual(response.status_code, 200)
        # Second product inserted with same id
        response2 = requests.request("POST", url, headers=headers, data=payload)
        self.assertEqual(response2.status_code, 409)

    def test_get_products(self):
        url = "http://localhost:5000/products"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        self.assertEqual(response.status_code, 200)

    def test_get_products_by_name(self):
        url = "http://localhost:5000/products/test_name_item"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "No product corresponding to title test_name_item")

        url2 = "http://localhost:5000/products/food"

        response = requests.request("GET", url, headers=headers, data=payload)
        self.assertEqual(response.status_code, 200)

    def test_get_titles(self):
        url = "http://localhost:5000/titles"
        response = requests.request("GET", url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.text is not None)


if __name__ == '__main__':
    tests = unittest.main()


