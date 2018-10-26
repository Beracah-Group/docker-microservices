from flask_restful import Api
from flask import Blueprint


def create_users_bp():
    """Create user blueprint."""
    users_blueprint = Blueprint('users', __name__)
    users_api = Api(users_blueprint)

    from .users import Users
    from .models import User, Location
    users_api.add_resource(
        Users,
        '/users/',
        '/users/<string:user_id>/',
        resource_class_kwargs={'User': User, 'Location': Location})
    return users_blueprint
