# Creates mongobd collection and fills it with dataset
from pymongo import MongoClient
import json

dataset_filename = "test_dataset.json"
database_name = "product"
collection_name = "productmodel"

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