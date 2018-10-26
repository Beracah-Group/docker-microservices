import json
from src.tests.base import BaseTestCase
from src.api.models import User, Location


def seed_user_location():
    """Seed test data."""
    new_location = Location(name='new_location')

    testuser_1 = User(
                name="testuser",
                user_name="@testuser",
                photo="http://testuser.png",
                phone="2537095434",
                email="testuser@email.com",
                location=new_location
        )
    testuser_1.save()
    testuser_2 = User(
                name="testuser1",
                user_name="@testuser1",
                photo="http://testuser.png",
                phone="25370954341",
                email="testuser1@email.com",
                location=new_location
        )
    testuser_2.save()
    new_location.save()
    return new_location, testuser_1, testuser_2


class TestUserModel(BaseTestCase):
    """Test basic operation on user model."""

    def test_create_user(self):
        """Ensure we can create users."""
        new_user = User(
            name="testuser",
            user_name="@testuser",
            photo="http://testuser.png",
            phone="2537095434",
            email="testuser@email.com",
            location=Location(name="uganda")
        )

        self.assertTrue(new_user.save())
        self.assertTrue(
            new_user == User.query.filter_by(uid=new_user.uid).first()
        )

    def test_delete_user(self):
        """Ensure we can delete users."""
        new_user = User(
            name="testuser",
            user_name="@testuser",
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
        new_location, testuser_1, testuser_2 = seed_user_location()
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
            user_name="@testuser",
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
        new_location, *users = seed_user_location()
        self.assertTrue(new_location.users)
        self.assertTrue(new_location.users[0])  # test we can index
        self.assertTrue(len(new_location.users) == len(users))


class TestUserResourceGet(BaseTestCase):
    """Test user GET verb work correctly."""

    def test_get_all_users(self):
        """Ensure we can retrive all users."""
        new_location, *users = seed_user_location()
        with self.client:
            response = self.client.get('/api/v1/users/')
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertListEqual(
                [user.serialize() for user in users], data['users']
            )
            self.assertEqual(
                data['message'],
                'Successfully retrived all users'
            )

    def test_get_user_by_id(self):
        """Ensure we can retrive a by id user."""
        new_location, user, _ = seed_user_location()
        with self.client:
            response = self.client.get(f'/api/v1/users/{user.uid}')
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                user.serialize(), data['user']
            )
            self.assertEqual(
                data['message'],
                'Successfully retrived user'
            )

    def test_get_user_by_email(self):
        """Ensure we can retrive a by email user."""
        new_location, user, _ = seed_user_location()
        with self.client:
            response = self.client.get(f'/api/v1/users?email={user.email}')
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                user.serialize(), data['user']
            )
            self.assertEqual(
                data['message'],
                'Successfully retrived user'
            )

    def test_get_user_by_username(self):
        """Ensure we can retrive a by username user."""
        new_location, user, _ = seed_user_location()
        with self.client:
            response = self.client.get(
                f'/api/v1/users?username={user.user_name}'
            )
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                user.serialize(), data['user']
            )
            self.assertEqual(
                data['message'],
                'Successfully retrived user'
            )

    def test_get_non_existent_user_404(self):
        """Ensure we get 404 when user does not exist."""
        with self.client:
            uid = "U-kdkadm-fnf-wewrm-34r"
            response = self.client.get(
                f'/api/v1/users/{uid}'
            )
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 404)
            self.assertEqual(
                data['message'],
                f'User {uid} not found'
            )


class TestUserResourcePost(BaseTestCase):
    """Test user POST verb work correctly."""

    def test_create_user(self):
        """Ensure user can be cretaed via web api."""
        new_location = Location(name='new_location')
        new_location.save()
        user_data = {
            'name': 'testuser',
            'username': '@testuser',
            'email': 'testuser@email.com',
            'phone': '23579789045',
            'photo': 'http://testuser.jpg',
            'location': new_location.uid
        }

        with self.client:
            response = self.client.post(
                f'/api/v1/users/',
                data=json.dumps(user_data),
                content_type='application/json'
            )
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data['user']['email'], user_data['email'])
            self.assertEqual(data['user']['phone'], user_data['phone'])
            self.assertEqual(
                data['message'],
                'User created succefully'
            )

    def test_empty_payload(self):
        """Ensure empty payload is rejected."""
        with self.client:
            response = self.client.post(
                f'/api/v1/users/',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                data['message'],
                'Please pass in name, username, phone, email, location'
            )

    def test_duplicate_user(self):
        """Ensure duplicate user can't be created."""
        new_location, user, _ = seed_user_location()

        user_data = dict(
                    name="testuser",
                    user_name="@testuser",
                    photo="http://testuser.png",
                    phone="2537095434",
                    email="testuser@email.com",
                    location=new_location.uid
            )
        with self.client:
            response = self.client.post(
                f'/api/v1/users/',
                data=json.dumps(user_data),
                content_type='application/json'
            )
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                data['message'],
                'User with some of those credetials already exists.'
            )
