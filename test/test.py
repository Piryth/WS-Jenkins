import json
import unittest

import requests


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    # We test directly the REST endpoint that calls the GraphQL endpoint
    def test_titles_api(self):
        res = requests.get("http://localhost:5000/titles")
        data = json.loads(res.content)
        print(data)


if __name__ == '__main__':
    unittest.main()
