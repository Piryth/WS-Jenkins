import json
import unittest

import requests


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here


        def test_titles_insert(self):
            data = {
                "id": "1000",
                "title": "food",
                "cost": 100
            }
            res = requests.post("http://localhost:5000/products", data)
            data = json.loads(res.content)
            print(data)

            res = requests.get("http://localhost:5000/titles")
            data = json.loads(res.content)
            print(data)


if __name__ == '__main__':
    unittest.main()
