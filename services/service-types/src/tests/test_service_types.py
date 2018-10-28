import unittest

# parses json to string or files (or python dict and []
import json

import os

import json
from src.tests.base import BaseTestCase
from src.api.models import Servicetypes

'''
 201  ok resulting to  creation of something
 200  ok
 400  bad request
 404  not found
 401  unauthorized
 409  conflict
'''


def seed_mode():
    """Seed test data."""
    new_mode = Servicetypes(name='new_mode')

    mode_1 = Servicetypes(
                mode="Self Drop",
                description="You drop your car and wait as it's being worked on",
        )
    mode_1.save()
    mode_2 = Servicetypes(
                mode="Pick & Drop",
                description="We pick your car, have it worked on and later return it",
        )
    mode_2.save()
    mode_3 = Servicetypes(
                mode="Home / Office service",
                description="We service your car from your place of convenience i.e home or office",
        )
    mode_3.save()
    new_package.save()
    return new_mode, mode_2, mode_3


class TestServicetypesModel(BaseTestCase):
    """Test basic operation on mode model."""

    def test_create_mode(self):
        """Ensure we can create package."""
        new_mode = Servicetypes(
            mode="Self Drop",
            description="You drop your car and wait as it's being worked on",
        )

        self.assertTrue(new_mode.save())
        self.assertTrue(
            new_mode == Servicepackages.query.filter_by(name="Self Drop").first()
        )

    def test_delete_package(self):
        """Ensure we can delete servicing mode."""
        new_mode = Servicetypes(
            mode="Pick & Drop",
            description="We pick your car, have it worked on and later return it",
        )

        new_mode.save()

        mode = Servicetypes.query.filter_by(name="Pick & Drop").first()
        self.assertTrue(mode.delete())
        self.assertFalse(Servicetypes.query.filter_by(name="Pick & Drop").first())