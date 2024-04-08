import json
import os

import requests
from bson.json_util import dumps
from dotenv import load_dotenv
from flask import Flask, request
from flask_restful import Api
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)
load_dotenv()

secret_key = "loremipsumdolorsitamet"
database = os.getenv("MONGO_TESTING_DATABASE")
titles = os.getenv("TITLES_API_URL")


@app.route("/products", methods=["GET"])
def get_all_products():
    client = MongoClient(database)
    db = client.WSCA
    products = db.Products
    res = dumps(products.find())

    return json.loads(res)


@app.route("/products/<title>", methods=["GET"])
def get_product_by_title(title):
    client = MongoClient(database)
    products = client.WSCA.Products

    res = dumps(products.find_one({"title": title}))

    if res == "null":
        return "No product corresponding to title " + title, 200
    return json.loads(res)


@app.route("/products", methods=["POST"])
def insert_product():
    # Init client
    client = MongoClient(database)
    product = client.WSCA.Products

    # Verifying content type
    if request.headers.get('Content-Type') != 'application/json':
        return "Content-Type not supported", 415

    secret = request.args.get('secret')
    print('secret is ', secret)
    if secret_key != secret:
        return "Unauthorized : the secret is invalid", 403

    record = json.loads(request.data)

    # Data safety check
    id = record.get('id', "")
    title = record.get('title', "")
    # It is okay if the price is not specified.
    cost = record.get('cost', 'undefined')
    if id == "" or title == "":
        return "Error : incorrect request", 400

    # Duplicate on id check
    res = product.find_one({"id": id})

    if res:
        print("conflit")
        return "Conflict : a product with the specified id exists", 409

    product.insert_one({'id': id, 'title': title, 'cost': cost})
    return "Product inserted"


@app.route("/products/<title>", methods=["DELETE"])
def delete_product(title):
    client = MongoClient(database)
    product = client.WSCA.Products

    secret = request.args.get('secret')
    print('secret is ', secret)
    if secret_key != secret:
        return "Unauthorized : the secret is invalid", 403

    product.delete_one({"title": title})

    return "Product deleted"


@app.route("/titles", methods=['GET'])
def get_titles():
    # GraphQL query
    ql_query = """{
    titles
    }
    """
    body = {"query": ql_query}

    res = requests.post(titles + "/graphql", dumps(body))
    if res.status_code != 200:
        return "Server internal error on GraphQL server", 500

    return json.loads(res.content), 200


@app.route('/', methods=['GET'])
def get_specification():
    try:
        with open('documentation.json', 'r') as file:
            specification = json.loads(file.read())
    except FileNotFoundError:
        return "Error when reading specification", 500

    return {"specification": specification}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
