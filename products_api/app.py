import json

import requests
from bson.json_util import dumps
from flask import Flask, request
from flask_api import status
from flask_restful import Api
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

secret_key = "loremipsumdolorsitamet"


@app.route("/products", methods=["GET"])
def get_all_products():
    client = MongoClient("mongodb://localhost:27017/")
    db = client.WSCA
    products = db.Products
    res = dumps(products.find())

    return json.loads(res)


@app.route("/products/<title>", methods=["GET"])
def get_product_by_title(title):
    client = MongoClient("mongodb://localhost:27017")
    products = client.WSCA.Products

    res = dumps(products.find_one({"title": title}))

    if res == "null":
        return "No product corresponding to title " + title, status.HTTP_200_OK
    return json.loads(res)


@app.route("/products", methods=["POST"])
def insert_product():
    # Init client
    client = MongoClient("mongodb://localhost:27017")
    product = client.WSCA.Products

    # Verifying content type
    if request.headers.get('Content-Type') != 'application/json':
        return "Content-Type not supported", status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

    secret = request.args.get('secret')
    print('secret is ', secret)
    if secret_key != secret:
        return "Unauthorized : the secret is invalid", status.HTTP_403_FORBIDDEN

    record = json.loads(request.data)

    # Data safety check
    id = record.get('id', "")
    title = record.get('title', "")
    # It is okay if the price is not specified.
    cost = record.get('cost', 'undefined')
    if id == "" or title == "":
        return "Error : incorrect request", status.HTTP_400_BAD_REQUEST

    # Duplicate on id check
    res = product.find_one({"id": id})

    if res:
        print("conflit")
        return "Conflict : a product with the specified id exists", status.HTTP_409_CONFLICT

    product.insert_one({'id': id, 'title': title, 'cost': cost})
    return "Product inserted"


@app.route("/products/<title>", methods=["DELETE"])
def delete_product(title):
    client = MongoClient("mongodb://localhost:27017")
    product = client.WSCA.Products

    secret = request.args.get('secret')
    print('secret is ', secret)
    if secret_key != secret:
        return "Unauthorized : the secret is invalid", status.HTTP_403_FORBIDDEN

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

    res = requests.post("http://localhost:5050/graphql", dumps(body))
    if res.status_code != 200:
        return "Server internal error on GraphQL server", status.HTTP_500_INTERNAL_SERVER_ERROR

    return json.loads(res.content), status.HTTP_200_OK
@app.route('/', methods=['GET'])
def get_specification():

    try:
        with open('documentation.json', 'r') as file:
            specification = json.loads(file.read())
    except FileNotFoundError:
        return "Error when reading specification", status.HTTP_500_INTERNAL_SERVER_ERROR

    return {"specification": specification}

if __name__ == '__main__':
    app.run(debug=True)
