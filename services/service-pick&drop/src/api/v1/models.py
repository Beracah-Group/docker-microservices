# import modules
from datetime import datetime

from src.api.__init__ import databases

# washing class model with methods
class Pickanddrop(databases.Model):
    __tablename__ = 'Pickanddrop'
    id = databases.Column(databases.Integer, primary_key=True, autoincrement=True)
    name = databases.Column(databases.String(20))
    price = databases.Column(databases.Integer)
    description = databases.Column(databases.String(300))
    date_created = databases.Column(databases.DateTime, default=datetime.utcnow())
    date_modified = databases.Column(databases.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    type = databases.Column(databases.String(50))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'Pickanddrop'
    }

    def save(self):
        databases.session.add(self)
        databases.session.commit()

    def to_json(self):
        return {
                'id': self.id,
                'name': self.name,
                'price': self.price,
                'description': self.description
            }

class Pickdrop(Pickanddrop):
    __mapper_args__ = {
        'polymorphic_identity': 'pickanddrop'
    }

class Selfdrop(Pickanddrop):
    __mapper_args__ = {
        'polymorphic_identity': 'selfdrop'
    }

class Homeservice(Pickanddrop):
    __mapper_args__ = {
        'polymorphic_identity': 'homeservice'
    }

    
    