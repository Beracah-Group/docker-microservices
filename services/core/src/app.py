import os
from flask import Flask


def create_app(config=None):
    """Create app with given config.

    args:
        config(): extra config
    returns:
        app(Flask): configured flask app instance
    """
    app = Flask(__name__)
    app.config.from_object(os.getenv('APP_SETTINGS'))

    app.url_map.strict_slashes = False  # diable redirects

    from src.api.models import database, User, Location
    database.init_app(app)

    @app.route('/')
    def health_check():
        return "Working fine", 200

    from src.api import create_users_bp
    app.register_blueprint(create_users_bp(), url_prefix='/api/v1')

    @app.shell_context_processor
    def ctx():
        return {
            'app': app,
            'db': database,
            'User': User,
            'Location': Location
        }
    return app
