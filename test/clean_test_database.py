import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

database = os.getenv("MONGO_TESTING_DATABASE")
if __name__ == '__main__':
    # Cleans test database
    client = MongoClient(database)
    db = client.WSCA
    products = db.Products
    products.delete_many({})
