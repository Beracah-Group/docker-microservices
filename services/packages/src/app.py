import os
from flask import Flask


def create_app(config=None):
    """
        args:
            config(): extra config
        returns:
            app(Flask): configured flask app instance
    """
    app = Flask(__name__)
    app.config.from_object(os.getenv('APP_SETTINGS'))

    from src.api.models import database
    database.init_app(app)

    @app.route('/')
    def health_check():
        return "Packages service working fine!", 200

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': database}

    return app
