import json

import requests

if __name__ == '__main__':
    res = requests.get("http://localhost:5000/titles")
    data = json.loads(res.content)
    print(data)
