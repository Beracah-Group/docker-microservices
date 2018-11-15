from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

database = SQLAlchemy()

class Servicetypes(database.Model):
    
    __tablename__ = "servicetypes"

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    mode = database.Column(database.String(30), nullable=False)
    description = database.Column(database.String(120), nullable=False)

    def __init__(self, mode):
        self.mode = mode
        self.description = description

    def save(self):
        database.session.add(self)
        database.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'mode': self.mode
        }