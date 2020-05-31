from flask import Flask
from flask_restful import Resource, reqparse, Api
from base import Rentals, db

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

db.init_app(app)
app.app_context().push()
db.create_all()

class Rentals_List(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=int, required=False, help='Price of the listing')
    parser.add_argument('bed', type=int, required=False, help='Number of beds in the listing')
    parser.add_argument('bath', type=int, required=False, help='Number of baths in the listing')
    parser.add_argument('sqft', type=int, required=False, help='Area of the listing')
    parser.add_argument('pet', type=int, required=False, help='Pets allowed or not')
    parser.add_argument('type', type=str, required=False, help='Type of the listing')
    parser.add_argument('last_update', type=str, required=False, help='When the listing was last updated')
    parser.add_argument('contact', type=str, required=False, help='Contact information for the listing')

    def get(self, address):
        item = Rentals.find_by_address(address)
        if item:
            return item.json()
        return {'Message': 'Rental not found'}

    def post(self, address):
        if Rentals.find_by_address(address):
            return {'Message': 'Rental with the  address {} already exists'.format(address)}

        args = Rentals_List.parser.parse_args()
        item = Rentals(address, args['price'], args['bed'], args['bath'], args['sqft'], args['pet'], args['type'], args['last_update'], args['contact'])

        item.save_to()
        return item.json()

    def put(self, address):
        args = Rentals_List.parser.parse_args()
        item = Rentals.find_by_address(address)
        if item:
            item.price = args['price']
            item.bed = args['bed']
            item.bath = args['bath']
            item.sqft = args['sqft']
            item.pet = args['pet']
            item.type = args['type']
            item.last_update = args['last_update']

        item = Rentals(address, args['price'], args['bed'], args['bath'], args['sqft'], args['pet'], args['type'], args['last_update'], args['contact'])
        item.save_to()

        return item.json()

    def delete(self, address):
        item = Rentals.find_by_address(address)
        if item:
            item.delete_()
            return {'Message': '{} has been deleted from database'.format(rental)}

        return {'Message': '{} cannot be found in the database'.format()}


class All_Rentals(Resource):
    def get(self):
        return {'Rentals': list(map(lambda x: x.json(), Rentals.query.all()))}

api.add_resource(All_Rentals, '/')
api.add_resource(Rentals_List, '/<string:address>')

if __name__=='__main__':
    app.run()
