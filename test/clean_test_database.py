from pymongo import MongoClient

if __name__ == '__main__':
    # Cleans test database
    client = MongoClient("mongodb+srv://admin:admin@cluster0.k8uei0j.mongodb.net/WS")
    db = client.WSCA
    products = db.Products
    products.delete_many({})