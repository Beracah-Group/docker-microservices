"""CLI commands for apps."""
import unittest
from flask.cli import FlaskGroup

from src.app import create_app
from src.api.models import database

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def recreate_db():
    database.drop_all()
    database.create_all()
    database.session.commit()


@cli.command()
def test():
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('src/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    cli()
