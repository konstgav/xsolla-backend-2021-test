# Creates mongobd collection and fills it with dataset
from pymongo import MongoClient
import json
import os

dataset_filename = "test_dataset.json"
database_name = "product"
collection_name = "productmodel"

password = os.environ.get("MONGO_PASSWD")
if password:
    client = MongoClient("mongodb+srv://konst:"+password+"@cluster0.73r12.mongodb.net/product?retryWrites=true&w=majority")
else:
    client = MongoClient()
db = client[database_name]
collection = db[collection_name]
collection.drop()
collection = db[collection_name]
with open(dataset_filename) as f:
    file_dataset = json.load(f)
    collection.insert_many(file_dataset)

docs = collection.find()
print('Test dataset:')
for doc in docs:
    print(doc)

client.close()