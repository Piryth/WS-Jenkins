import json

from bson.json_util import dumps
from flask import request
from pymongo import MongoClient

from app import app


@app.route("/products", methods=["GET"])
def get_all_products():
    client = MongoClient("mongodb://localhost:27017/")
    db = client.WSCA
    products = db.Products
    res = dumps(products.find())

    return json.loads(res)


@app.route("/products/<name>", methods=["GET"])
def get_product_by_name(name):
    client = MongoClient("mongodb://localhost:27017")
    products = client.WSCA.Products

    print(name)
    res = dumps(products.find_one({"name": name}))

    print(res)

    if res == "null":
        return "No product corresponding to name " + name
    return json.loads(res)


@app.route("/products", methods=["POST"])
def insert_product():
    record = json.loads(request.data)

    client = MongoClient("mongodb://localhost:27017")
    product = client.WSCA.Products

    print(record)

    product.insert_one(record)
    return "Product inserted"


@app.route("/products", methods=["DELETE"])
def delete_product():
    client = MongoClient("mongodb://localhost:27017")
    product = client.WSCA.Products

    record = json.loads(request.data)
    name = record["name"]

    product.delete_one({"name": name})

    return "Product deleted"
