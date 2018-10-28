import unittest

# parses json to string or files (or python dict and []
import json

import os

import json
from src.tests.base import BaseTestCase
from src.api.models import Servicepackages

'''
 201  ok resulting to  creation of something
 200  ok
 400  bad request
 404  not found
 401  unauthorized
 409  conflict
'''


def seed_package():
    """Seed test data."""
    new_package = Servicepackages(name='new_package')

    package_1 = Servicepackages(
                name="basic",
                price= 56000,
                description="Oil change, break pad, more mileage",
        )
    package_1.save()
    package_2 = Servicepackages(
                name="standard",
                price= 96000,
                description="Oil change, break pad, more mileage and more",
        )
    package_2.save()
    package_3 = Servicepackages(
                name="enhanced",
                price= 96000,
                description="Oil change, break pad, more mileage and even much more",
        )
    package_2.save()
    new_package.save()
    return new_package, package_1, package_2


class TestServicepackagesModel(BaseTestCase):
    """Test basic operation on packages model."""

    def test_create_package(self):
        """Ensure we can create package."""
        new_package = Servicepackages(
            name="enhanced",
            price= 96000,
            description="Oil change, break pad, more mileage and even much more",
        )

        self.assertTrue(new_package.save())
        self.assertTrue(
            new_package == Servicepackages.query.filter_by(name="enhanced").first()
        )

    def test_delete_package(self):
        """Ensure we can delete package."""
        new_package = Servicepackages(
            name="enhanced",
            price= 96000,
            description="Oil change, break pad, more mileage and even much more",
        )

        new_package.save()

        package = Servicepackages.query.filter_by(name="enhanced").first()
        self.assertTrue(package.delete())
        self.assertFalse(Servicepackages.query.filter_by(name="enhanced").first())