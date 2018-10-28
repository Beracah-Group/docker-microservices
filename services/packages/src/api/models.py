from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

database = SQLAlchemy()

class Servicepackages(db.Model):
    
    __tablename__ = "servicepackages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Integer nullable=False)
    description = db.Column(db.String(120), nullable=False)

    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
            'price': self.price
            'description': self.description
        }