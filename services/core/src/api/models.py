import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError

database = SQLAlchemy()


def generate_uid(prefix="U"):
    return prefix + '-' + str(uuid.uuid1())


class Base(database.Model):

    __abstract__: bool = True

    uid = database.Column(
        database.String(128),
        primary_key=True,
        default=generate_uid
    )

    name = database.Column(database.String, nullable=False)
    created_at = database.Column(database.DateTime, default=func.now())
    updated_at = database.Column(database.DateTime, onupdate=func.now())

    def save(self):
        try:
            database.session.add(self)
            database.session.commit()
            return True
        except SQLAlchemyError as e:
            database.session.rollback()
            print(e)
        return False

    def delete(self):
        try:
            database.session.delete(self)
            database.session.commit()
            deleted = True
        except Exception as e:
            deleted = False
            database.session.rollback()
            print(e)
        return deleted

    def serialize(self, exclude={}):
        """Map object to dict representation."""
        instance_attribute_value_pair = {
            column.name: str(getattr(self, column.name))
            for column in self.__table__.columns if column.name not in exclude
        }

        return instance_attribute_value_pair


class Location(Base):

    __tablename__: str = 'locations'

    users = database.relationship(
        'User',
        back_populates='location',
        cascade='all, delete, delete-orphan'
    )


class User(Base):

    __tablename__: str = 'users'

    location_id = database.Column(
        database.String(128),
        database.ForeignKey('locations.uid'),
        nullable=False
    )

    location = database.relationship('Location', back_populates='users')

    email = database.Column(database.String, nullable=False, unique=True)
    phone = database.Column(database.String, nullable=False, unique=True)
    photo = database.Column(database.String)
    user_name = database.Column(
        database.String(128),
        nullable=False,
        unique=True
    )
