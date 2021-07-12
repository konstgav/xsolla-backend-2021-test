from flask import Flask, jsonify
from flask_restful import reqparse, Api, Resource, fields, marshal_with
from flask_mongoengine import MongoEngine

application = Flask(__name__)
api = Api(application)
application.config['MONGODB_SETTINGS'] = {
    'db': 'product',
    'host': 'mongo-host',
    'port': 27017
}
db = MongoEngine()
db.init_app(application)

class ProductModel(db.Document):
    _id = db.IntField()
    sku = db.StringField()
    name = db.StringField()
    type = db.StringField()
    price = db.IntField()
    meta = {'collection': 'productmodel'}

def get_product_or_abort(id):
    product = ProductModel.objects.get_or_404(_id=id)
    return product

parser = reqparse.RequestParser()
parser.add_argument('_id', type=int, help='id must be integer')
parser.add_argument('sku', type=str)
parser.add_argument('name', type=str)
parser.add_argument('type', type=str)
parser.add_argument('price', type=int, help='price must be integer')

paginator_parser = reqparse.RequestParser()
paginator_parser.add_argument('page', type=int, help='page must be integer')
paginator_parser.add_argument('limit_per_page', type=int, help='limit_per_page must be integer')

resource_fields = {
    '_id': fields.Integer,
    'sku': fields.String,
    'name': fields.String,
    'type': fields.String,
    'price': fields.Integer
}

@application.route('/')
def index():
    return jsonify(
        status=True,
        message='Welcome to the Dockerized Flask MongoDB app !'
    )

# Shows a single product item, lets you delete a product item, create a new product item
class Product(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        product = get_product_or_abort(id)
        return product
        
    @marshal_with(resource_fields)
    def delete(self, id):
        #product = get_product_or_abort(id)
        #product.delete()
        ProductModel.objects(_id=id).delete()
        return f'Product with id = {id} deleted!', 204

    @marshal_with(resource_fields)
    def put(self, id):
        product = get_product_or_abort(id)
        args = parser.parse_args()
        if args['sku']:
            ProductModel.objects(_id=id).update(sku = args['sku'])
        if args['name']:
            ProductModel.objects(_id=id).update(name = args['name'])
        if args['type']:
            ProductModel.objects(_id=id).update(type = args['type'])
        if args['price']:
            ProductModel.objects(_id=id).update(price = args['price'])
        product = get_product_or_abort(id)
        return product, 200

# Shows a list of all products and lets you POST to add new product
class ProductsList(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = paginator_parser.parse_args()
        print(args)
        page = 1
        if args['page']:
            page = args['page']
        limit = 10
        if args['limit_per_page']:
            limit = args['limit_per_page']
            print(limit) 
        products = ProductModel.objects.paginate(page=page, per_page=limit)
        return products.items, 200
        
    @marshal_with(resource_fields)
    def post(self):
        id = ProductModel.objects().order_by("-_id").limit(-1).first()["_id"] + 1
        args = parser.parse_args()
        product = ProductModel(_id=id, sku=args['sku'], name=args['name'], type=args['type'], price=args['price']).save()
        return product, 201

## Setup the API resource routing
api.add_resource(Product, '/product/<int:id>')
api.add_resource(ProductsList, '/products')

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000, debug=True)