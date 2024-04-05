import json

import requests

if __name__ == '__main__':
    data = {
        "id": "1000",
        "title": "food",
        "cost": 100
    }
    res = requests.post("http://localhost:5000/products", data)
    data = json.loads(res.content)
    print(data)
