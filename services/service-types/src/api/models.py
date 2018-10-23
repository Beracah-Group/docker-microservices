from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

database = SQLAlchemy()

class Servicetypes(db.Model):
    
    __tablename__ = "servicetypes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mode = db.Column(db.String(30), nullable=False)

    def __init__(self, mode):
        self.mode = mode

    def to_json(self):
        return {
            'id': self.id,
            'mode': self.mode
        }