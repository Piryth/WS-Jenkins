from json import loads

import graphene
from flask import Flask, request
from pymongo import MongoClient


class Product(graphene.ObjectType):
    id = graphene.ID()
    title = graphene.String()
    cost = graphene.String()


class Query(graphene.ObjectType):
    products = graphene.List(Product)
    titles = graphene.List(graphene.String)

    def resolve_products(self, info):
        client = MongoClient("mongodb+srv://admin:admin@cluster0.k8uei0j.mongodb.net/WS")
        db = client.WSCA
        products = db.Products
        res = list(products.find())
        print(res)
        return [Product(product.get('id'), product.get('title'), product.get('cost')) for product in res]

    def resolve_titles(self, info):
        client = MongoClient("mongodb+srv://admin:admin@cluster0.k8uei0j.mongodb.net/WS")
        db = client.WSCA
        products = db.Products
        res = list(products.find())
        print(res)
        return [product.get('title') for product in res]


schema = graphene.Schema(query=Query)

app = Flask(__name__)


@app.route('/graphql', methods=['POST'])
def graphql_query():
    # str to dict
    data = loads(request.data)
    query = data.get('query')
    print(query)
    result = schema.execute(query)
    print(result.data)
    return result.data


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=False)
