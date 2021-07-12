import unittest
from warnings import catch_warnings
import requests
import prepare_mongo

server = 'localhost:5000'

class ApiTest(unittest.TestCase):
    def test_read(self):
        id = 0
        try:
            response = requests.get('http://'+server+'/product/'+str(id))
            self.assertEqual(response.json()["name"], 'tank')
        except:
            self.fail("Failed to establish a new connection")
 
    def test_read_all(self):
        try:
            limit_per_page = 2
            response = requests.get('http://'+server+'/products', params={'page': 1, 'limit_per_page': limit_per_page})
            self.assertEqual(len(response.json()), limit_per_page)
            self.assertEqual(response.json()[1]["name"], 'coin')
        except:
            self.fail("Failed to establish a new connection")

    def test_delete(self):
        id = 3
        try:
            response = requests.delete('http://'+server+'/product/'+str(id))
            collection = prepare_mongo.collection
            self.assertEqual(collection.count_documents({}), 5)
            prepare_mongo.client.close()
        except:
            self.fail("Failed to establish a new connection")

    def test_update(self):
        id = 1
        try:
            response = requests.put('http://'+server+'/product/'+str(id), data={"name":"lucky coin", "price":9})
            collection = prepare_mongo.collection
            self.assertEqual(collection.find_one({"name": "lucky coin"})["_id"], 1)
            prepare_mongo.client.close()
        except:
            self.fail("Failed to establish a new connection")

    def test_post(self):
        try:
            response = requests.post('http://'+server+'/products', data={"name":"gun", "sku":"g8", "type":"item", "price":3})
            collection = prepare_mongo.collection
            self.assertTrue(collection.find_one({"name": 'gun'}))
            prepare_mongo.client.close()
        except:
            self.fail("Failed to establish a new connection")

if __name__ == '__main__':
    unittest.main()