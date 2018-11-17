import unittest

# parses json to string or files (or python dict and []
import json

# from config file
from src.api.__init__ import app, EnvironmentName, databases

'''
 201  ok resulting to  creation of something
 200  ok
 400  bad request
 404  not found
 401  unauthorized
 409  conflict
'''


# tests all functionality of pd.py and there defined methods
class PickanddropTestCases(unittest.TestCase):
    # testing client using testing environment
    def setUp(self):
        self.app = app.test_client()
        EnvironmentName('TestingEnvironment')
        databases.create_all()

        # creating a pd for testing purpose
        self.payloads = json.dumps({'name': 'Pick and drop', 'price': 5000, 'description': 'Bring and take car yourself'})

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    # tests that a pd is successfully created
    def test_create_new_pd_package(self):
        response = self.app.post('/pickanddrop/api/v1/pickanddrop', data=self.payloads)
        self.assertTrue(response.status_code == 201)
        self.assertIn('Pick and drop mode added successfully', response.data.decode('utf-8'))

    # tests creation of pd model fails without name
    def test_create_new_pd_without_name(self):
        payload = json.dumps({'name': ''})
        response = self.app.post('/pickanddrop/api/v1/pickanddrop', data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Pick and drop mode has no name', response.data.decode('utf-8'))

    # tests creation of pd model fails without price
    def test_create_new_pd_without_price(self):
        payload = json.dumps({'price': '', 'name': 'Self drop'})
        response = self.app.post('/pickanddrop/api/v1/pickanddrop', data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Pick and drop mode has no price tag', response.data.decode('utf-8'))

    # tests creation of pd model fails without description
    def test_create_new_pd_without_description(self):
        payload = json.dumps({'description': '', 'price': 7000, 'name': 'Home service'})
        response = self.app.post('/pickanddrop/api/v1/pickanddrop', data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Pick and drop mode has no description', response.data.decode('utf-8'))

    # tests creation of pd fails with existing name
    def test_create_existing_pd_model(self):
        response = self.app.post('/pickanddrop/api/v1/pickanddrop', data=self.payloads)
        response = self.app.post('/pickanddrop/api/v1/pickanddrop', data=self.payloads)
        self.assertIn('this Pick and drop mode already exists', response.data.decode('utf-8'))

    # tests that a pd successfully created is retrieved
    def test_get_pd_package(self):
        response = self.app.post('/pickanddrop/api/v1/pickanddrop', data=self.payloads)
        response = self.app.get('/pickanddrop/api/v1/pickanddrop')
        self.assertEqual(response.status_code, 200)

    # tests that a pd not successfully created is not found
    def test_get_pd_while_database_empty(self):
        response = self.app.get('/pickanddrop/api/v1/pickanddrop')
        self.assertTrue(response.status_code == 200)
        self.assertIn('No Pick and drop mode has been created yet', response.data.decode('utf-8'))

    # tests getting a pd type by id
    def test_get_pd_package_by_id(self):
        response = self.app.post('/pickanddrop/api/v1/pickanddrop', data=self.payloads)
        response = self.app.get('/pickanddrop/api/v1/pickanddrop/1')
        self.assertEqual(response.status_code, 200)

    # tests getting a pd by invalid id fails
    def test_get_pd_by_invalid_id(self):
        response = self.app.post('/pickanddrop/api/v1/pickanddrop', data=self.payloads)
        response = self.app.get('/pickanddrop/api/v1/pickanddrop/8')
        self.assertEqual(response.status_code, 404)

    # tests updating a pd
    def test_update_pd(self):
        response = self.app.post('/pickanddrop/api/v1/pickanddrop', data=self.payloads)
        payload = json.dumps({'name': 'Home', 'price': 6000, 'description': 'In the comfort of your home or at office parkin'})
        response = self.app.put('/pickanddrop/api/v1/pickanddrop/1', data=payload)
        self.assertEqual(response.status_code, 201)

    # tests updating a non existent pd fails
    def test_update_non_existence_pd(self):
        response = self.app.post('/pickanddrop/api/v1/pickanddrop', data=self.payloads)
        payload = json.dumps({'name': 'Later'})
        response = self.app.put('/pickanddrop/api/v1/pickanddrop/3', data=payload)
        self.assertTrue(response.status_code == 404)

    # tests deleting a pd type
    def test_delete_pd(self):
        response = self.app.post('/pickanddrop/api/v1/pickanddrop', data=self.payloads)
        response = self.app.delete('/pickanddrop/api/v1/pickanddrop/1', data=self.payloads)
        self.assertTrue(response.status_code, 200)

    # tests deleting a non existent pd fails
    def test_delete_non_existence_pd(self):
        response = self.app.post('/pickanddrop/api/v1/pickanddrop', data=self.payloads)
        response = self.app.delete('/pickanddrop/api/v1/pickanddrop/3', data=self.payloads)
        self.assertTrue(response.status_code, 404)

    # tests that a pagination default is 3
    def test_get_pagination_default(self):
        response = self.app.get('/pickanddrop/api/v1/pickanddrop?limit=3')
        self.assertEqual(response.status_code, 200) 

    # tests search pd type by name
    def test_search_pd(self):
        response = self.app.post('/pickanddrop/api/v1/pickanddrop', data=self.payloads)
        response = self.app.get('/pickanddrop/api/v1/pickanddrop?q=Standard')
        self.assertEqual(response.status_code, 200)

    # tests search pd by name
    def test_search_non_existent_pd(self):
        response = self.app.post('/pickanddrop/api/v1/pickanddrop', data=self.payloads)
        response = self.app.get('/pickanddrop/api/v1/pickanddrop?q=Justbasic')
        self.assertIn('The Pick and drop mode you searched does not exist', response.data.decode('utf-8'))
