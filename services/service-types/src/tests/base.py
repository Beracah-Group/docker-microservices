from flask_testing import TestCase

from src.app import create_app
from src.api.models import database

app = create_app()


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('src.config.TestingConfig')
        return app

    def setUp(self):
        database.create_all()
        database.session.commit()

    def tearDown(self):
        database.session.remove()
        database.drop_all()
