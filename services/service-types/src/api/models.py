from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

database = SQLAlchemy()

class Servicetypes(db.Model):
    
    __tablename__ = "servicetypes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mode = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(120), nullable=False)

    def __init__(self, mode):
        self.mode = mode
        self.description = description

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'mode': self.mode
        }