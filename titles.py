import json

import graphene
import requests

from app import (app)


class Product(graphene.ObjectType):
    id = graphene.ID()
    title = graphene.String()
    price = graphene.Decimal()


class Query(graphene.ObjectType):
    products = graphene.Field(Product)


def resolve_products(root, info):
    data = requests.get("localhost:5000/products")


@app.route("/titles", methods=["GET"])
def get_titles():
    schema = graphene.Schema(query=Query)
    query = """
        {
            product {
                title
            }
        }
    """
    result = schema.execute(query)

    return json.dumps(result.data)
