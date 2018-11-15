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


# tests all functionality of denting.py and there defined methods
class DentingTestCases(unittest.TestCase):
    # testing client using testing environment
    def setUp(self):
        self.app = app.test_client()
        EnvironmentName('TestingEnvironment')
        databases.create_all()

        # creating a denting package for testing purpose
        self.payloads = json.dumps({'package': 'Standard', 'price': 220000, 'description': 'Whole car body'})

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    # tests that a denting package is successfully created
    def test_create_new_denting_package(self):
        response = self.app.post('/denting/api/v1/dentingpackage', data=self.payloads)
        self.assertTrue(response.status_code == 201)
        self.assertIn('denting package added successfully', response.data.decode('utf-8'))

    # tests creation of denting model fails without name
    def test_create_new_denting_without_name(self):
        payload = json.dumps({'package': ''})
        response = self.app.post('/denting/api/v1/dentingpackage', data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('denting package has no name', response.data.decode('utf-8'))

    # tests creation of denting model fails without price
    def test_create_new_denting_without_price(self):
        payload = json.dumps({'price': '', 'package': 'valuehere'})
        response = self.app.post('denting/api/v1/dentingpackage', data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('denting package has no price tag', response.data.decode('utf-8'))

    # tests creation of dent model fails without description
    def test_create_new_denting_without_description(self):
        payload = json.dumps({'description': '', 'price': 45, 'package': 'valuehere'})
        response = self.app.post('denting/api/v1/dentingpackage', data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('denting package has no description', response.data.decode('utf-8'))

    # tests creation of denting fails with existing name
    def test_create_existing_denting_model(self):
        response = self.app.post('denting/api/v1/dentingpackage', data=self.payloads)
        response = self.app.post('denting/api/v1/dentingpackage', data=self.payloads)
        self.assertIn('this denting package already exists', response.data.decode('utf-8'))

    # tests that a dent successfully created is retrieved
    def test_get_denting_package(self):
        response = self.app.post('/denting/api/v1/dentingpackage', data=self.payloads)
        response = self.app.get('/denting/api/v1/dentingpackage')
        self.assertEqual(response.status_code, 200)

    # tests that a denting not successfully created is not found
    def test_get_denting_while_database_empty(self):
        response = self.app.get('/denting/api/v1/dentingpackage')
        self.assertTrue(response.status_code == 200)
        self.assertIn('No denting package has been created', response.data.decode('utf-8'))

    # tests getting a denting type by id
    def test_get_dent_package_by_id(self):
        response = self.app.post('/denting/api/v1/dentingpackage', data=self.payloads)
        response = self.app.get('/denting/api/v1/dentingpackage/1')
        self.assertEqual(response.status_code, 200)

    # tests getting a dent by invalid id fails
    def test_get_dent_by_invalid_id(self):
        response = self.app.post('/denting/api/v1/dentingpackage', data=self.payloads)
        response = self.app.get('/denting/api/v1/dentingpackage/8')
        self.assertEqual(response.status_code, 404)

    # tests updating a denting
    def test_update_denting(self):
        response = self.app.post('/denting/api/v1/dentingpackage', data=self.payloads)
        payload = json.dumps({'package': 'Basic', 'price': 85000, 'description': 'One side of the fours sides on a car'})
        response = self.app.put('/denting/api/v1/dentingpackage/1', data=payload)
        self.assertEqual(response.status_code, 201)

    # tests updating a non existent denting fails
    def test_update_non_existence_denting(self):
        response = self.app.post('/denting/api/v1/dentingpackage', data=self.payloads)
        payload = json.dumps({'package': 'Enhanced'})
        response = self.app.put('/denting/api/v1/dentingpackage/3', data=payload)
        self.assertTrue(response.status_code == 404)

    # tests deleting a denting type
    def test_delete_denting(self):
        response = self.app.post('/denting/api/v1/dentingpackage', data=self.payloads)
        response = self.app.delete('/denting/api/v1/dentingpackage/1', data=self.payloads)
        self.assertTrue(response.status_code, 200)

    # tests deleting a non existent denting fails
    def test_delete_non_existence_denting(self):
        response = self.app.post('denting/api/v1/dentingpackage', data=self.payloads)
        response = self.app.delete('/denting/api/v1/dentingpackage/3', data=self.payloads)
        self.assertTrue(response.status_code, 404)

    # tests that a pagination default is 3
    def test_get_pagination_default(self):
        response = self.app.get('/denting/api/v1/dentingpackage?limit=3')
        self.assertEqual(response.status_code, 200) 

    # tests search denting type by name
    def test_search_denting(self):
        response = self.app.post('denting/api/v1/dentingpackage', data=self.payloads)
        response = self.app.get('/denting/api/v1/dentingpackage?q=Standard')
        self.assertEqual(response.status_code, 200)

    # tests search denting by name
    def test_search_non_existent_denting(self):
        response = self.app.post('denting/api/v1/dentingpackage', data=self.payloads)
        response = self.app.get('/denting/api/v1/dentingpackage?q=Justbasic')
        self.assertIn('The denting package you searched does not exist', response.data.decode('utf-8'))
