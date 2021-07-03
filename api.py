from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

# Generate test dataset 
PRODUCTS = [
    {'id': 0, 'sku': 'a0', 'name': 'tank', 'type': 'item', 'price': 124},
    {'id': 1, 'sku': 'a1', 'name': 'coin', 'type': 'item', 'price': 1},
    {'id': 2, 'sku': 'a2', 'name': 'rainbow', 'type': 'item', 'price': 200},
    {'id': 3, 'sku': 'a3', 'name': 't-shirt', 'type': 'merch', 'price': 5},
    {'id': 4, 'sku': 'a4', 'name': 'lipstick', 'type': 'merch', 'price': 6},
    {'id': 5, 'sku': 'a5', 'name': 'cup', 'type': 'merch', 'price': 4}
]

def abort_if_product_not_exist(id):
    if not any(product['id'] == id for product in PRODUCTS):
        abort(404, message = f"Product with id = {id} doesn't exist")

parser = reqparse.RequestParser()
parser.add_argument('id', type=int, help='id must be integer')
parser.add_argument('sku', type=str)
parser.add_argument('name', type=str)
parser.add_argument('type', type=str)
parser.add_argument('price', type=int, help='price must be integer')

# Shows a single product item, lets you delete a product item, create a new product item
class Product(Resource):
    def get(self, id):
        abort_if_product_not_exist(id)
        return next((product for product in PRODUCTS if product['id'] == id), None)

    def delete(self, id):
        abort_if_product_not_exist(id)
        for i in range(len(PRODUCTS)):
            if PRODUCTS[i]['id'] == id:
                del PRODUCTS[i]
                break
        return '', 204

    def put(self, id):
        abort_if_product_not_exist(id)
        args = parser.parse_args()
        for i in range(len(PRODUCTS)):
            if PRODUCTS[i]['id'] == id:
                if args['sku'] != None:
                    PRODUCTS[i]['sku'] = args['sku'] 
                if args['name'] != None:
                    PRODUCTS[i]['name'] = args['name']
                if args['type'] != None:
                    PRODUCTS[i]['type'] = args['type']
                if args['price'] != None:
                    PRODUCTS[i]['price'] = args['price']
                break
        return PRODUCTS[i], 201

# Shows a list of all products and lets you POST to add new product
class ProductList(Resource):
    def get(self):
        return PRODUCTS

    def post(self):
        id = max(product['id'] for product in PRODUCTS) + 1
        args = parser.parse_args()
        product = {'id': id, 'sku': args['sku'], 'name': args['name'], 'type': args['type'], 'price': args['price']}
        PRODUCTS.append(product)
        return product, 201

## Setup the Api resource routing
api.add_resource(Product, '/product/<int:id>')
api.add_resource(ProductList, '/products')

if __name__ == '__main__':
    app.run(debug = True)