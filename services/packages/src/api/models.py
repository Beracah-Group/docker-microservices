from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

database = SQLAlchemy()

class Servicepackages(database.Model):
    
    __tablename__ = "servicepackages"

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    name = database.Column(database.String(30), nullable=False)
    price = database.Column(database.Integer, nullable=False)
    description = database.Column(database.String(120), nullable=False)

    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description

    def save(self):
        database.session.add(self)
        database.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description
        }