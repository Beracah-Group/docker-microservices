import json
from src.tests.base import BaseTestCase
from src.api.models import User, Location


class TestUserModel(BaseTestCase):
    """Test basic operation on user model."""

    def test_create_user(self):
        """Ensure we can create users."""
        new_user = User(
            name="testuser",
            photo="http://testuser.png",
            phone="2537095434",
            email="testuser@email.com",
            location=Location(name="uganda")
        )

        self.assertTrue(new_user.save())
        self.assertTrue(new_user == User.query.filter_by(uid=new_user.uid).first())

    def test_delete_user(self):
        """Ensure we can delete users."""
        new_user = User(
            name="testuser",
            photo="http://testuser.png",
            phone="2537095434",
            email="testuser@email.com",
            location=Location(name="uganda")
        )

        new_user.save()

        user = User.query.filter_by(name="testuser").first()
        self.assertTrue(user.delete())
        self.assertFalse(User.query.filter_by(name="testuser").first())


class TestLocationModel(BaseTestCase):
    """Test basic operation on user model."""

    def test_create_location(self):
        """Ensure we can create Locations."""
        new_location = Location(name="new_location")

        self.assertTrue(new_location.save())
        self.assertTrue(new_location == Location.query.filter_by(
            uid=new_location.uid).first())

    def test_delete_location(self):
        """Ensure we can delete Locations."""
        new_location = Location(name="new_location")
        new_location.save()

        location = Location.query.filter_by(name="new_location").first()
        self.assertTrue(location.delete())
        self.assertFalse(Location.query.filter_by(name="testuser").first())

    def test_cascade_delete_works(self):
        """Ensure deleting a location deletes all users from that location."""
        new_location = Location(name='new_location')

        testuser_1 = User(
                name="testuser",
                photo="http://testuser.png",
                phone="2537095434",
                email="testuser@email.com",
                location=new_location
        )
        testuser_1.save()
        testuser_2 = User(
                name="testuser1",
                photo="http://testuser.png",
                phone="25370954341",
                email="testuser1@email.com",
                location=new_location
        )
        testuser_2.save()
        new_location.save()
        location = Location.query.filter_by(name="new_location").first()
        self.assertTrue(location.delete())
        self.assertFalse(User.query.all())


class TestUserLocationRelationship(BaseTestCase):
    """Test many to one relationship on Location User model."""

    def test_user_location_relationship(self):
        """Ensure user has one to many relationship with location."""
        kenya = Location(name='Kenya')
        kenya.save()

        new_user = User(
            name="testuser",
            photo="http://testuser.png",
            phone="2537095434",
            email="testuser@email.com",
            location=kenya
        )
        new_user.save()
        self.assertTrue(new_user.location)
        self.assertFalse(type(new_user.location) == type(Location))

    def test_location_user_relationship(self):
        """Ensure location has many to one relationship with users."""
        new_location = Location(name='new_location')

        users = [
            User(
                name="testuser",
                photo="http://testuser.png",
                phone="2537095434",
                email="testuser@email.com",
                location=new_location
            ),
            User(
                name="testuser1",
                photo="http://testuser.png",
                phone="25370954341",
                email="testuser1@email.com",
                location=new_location
            )
        ]

        new_location.save()

        self.assertTrue(new_location.users)
        self.assertTrue(new_location.users[0]) # test we can index
        self.assertTrue(len(new_location.users) == len(users))
