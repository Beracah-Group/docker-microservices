# import modules
from datetime import datetime

from src.api.__init__ import databases

# denting class model with methods
class Denting(databases.Model):
    __tablename__ = 'Denting'
    id = databases.Column(databases.Integer, primary_key=True, autoincrement=True)
    package = databases.Column(databases.String(20))
    price = databases.Column(databases.Integer)
    description = databases.Column(databases.String(300))
    date_created = databases.Column(databases.DateTime, default=datetime.utcnow())
    date_modified = databases.Column(databases.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def save(self):
        databases.session.add(self)
        databases.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'package': self.package,
            'price': self.price,
            'description': self.description
        }
