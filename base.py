from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Rentals(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    address = db.Column(db.String(100), unique=False, nullable=False)

    price = db.Column(db.Integer, unique=False, nullable=False)

    bed = db.Column(db.Integer, unique=False, nullable=True)

    bath = db.Column(db.Integer, unique=False, nullable=True)

    sqft = db.Column(db.Integer, unique=False, nullable=True)

    pet = db.Column(db.Integer, unique=False, nullable=True)

    type = db.Column(db.String(50), unique=False, nullable=False)

    last_updated = db.Column(db.String(100), unique=False, nullable=False)

    contact = db.Column(db.String(250), unique=False, nullable=False)

    def __init__(self, address, price, bed, bath, sqft, pet, type, last_updated, contact):
        self.address = address
        self.price = price
        self.bed = bed
        self.bath = bath
        self.sqft = sqft
        self.pet = pet
        self.type = type
        self.last_updated = last_updated
        self.contact = contact

    def json(self):
        return {}
