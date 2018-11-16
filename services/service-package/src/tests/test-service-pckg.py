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


# tests all functionality of servicepackage.py and there defined methods
class ServicepkgTestCases(unittest.TestCase):
    # testing client using testing environment
    def setUp(self):
        self.app = app.test_client()
        EnvironmentName('TestingEnvironment')
        databases.create_all()

        # creating a service package for testing purpose
        self.payloads = json.dumps({'name': 'Standard', 'price': 175000, 'description': 'Whole car servicing'})

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    # tests that a service package is successfully created
    def test_create_new_service_package(self):
        response = self.app.post('/servicepkg/api/v1/servicepkg', data=self.payloads)
        self.assertTrue(response.status_code == 201)
        self.assertIn('service package added successfully', response.data.decode('utf-8'))

    # tests creation of sp model fails without name
    def test_create_new_sp_without_name(self):
        payload = json.dumps({'name': ''})
        response = self.app.post('/servicepkg/api/v1/servicepkg', data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('service package has no name', response.data.decode('utf-8'))

    # tests creation of sp model fails without price
    def test_create_new_sp_without_price(self):
        payload = json.dumps({'price': '', 'name': 'Basic'})
        response = self.app.post('/servicepkg/api/v1/servicepkg', data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('service package has no price tag', response.data.decode('utf-8'))

    # tests creation of sp model fails without description
    def test_create_new_sp_without_description(self):
        payload = json.dumps({'description': '', 'price': 220000, 'name': 'Enhanced'})
        response = self.app.post('/servicepkg/api/v1/servicepkg', data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('service package has no description', response.data.decode('utf-8'))

    # tests creation of sp fails with existing name
    def test_create_existing_sp_model(self):
        response = self.app.post('/servicepkg/api/v1/servicepkg', data=self.payloads)
        response = self.app.post('/servicepkg/api/v1/servicepkg', data=self.payloads)
        self.assertIn('this service package already exists', response.data.decode('utf-8'))

    # tests that a sp successfully created is retrieved
    def test_get_service_package(self):
        response = self.app.post('/servicepkg/api/v1/servicepkg', data=self.payloads)
        response = self.app.get('/servicepkg/api/v1/servicepkg')
        self.assertEqual(response.status_code, 200)

    # tests that a sp not successfully created is not found
    def test_get_sp_while_database_empty(self):
        response = self.app.get('/servicepkg/api/v1/servicepkg')
        self.assertTrue(response.status_code == 200)
        self.assertIn('No service package has been created yet', response.data.decode('utf-8'))

    # tests getting a sp type by id
    def test_get_sp_package_by_id(self):
        response = self.app.post('/servicepkg/api/v1/servicepkg', data=self.payloads)
        response = self.app.get('/servicepkg/api/v1/servicepkg/1')
        self.assertEqual(response.status_code, 200)

    # tests getting a sp by invalid id fails
    def test_get_sp_by_invalid_id(self):
        response = self.app.post('/servicepkg/api/v1/servicepkg', data=self.payloads)
        response = self.app.get('/servicepkg/api/v1/servicepkg/8')
        self.assertEqual(response.status_code, 404)

    # tests updating a sp
    def test_update_sp(self):
        response = self.app.post('/servicepkg/api/v1/servicepkg', data=self.payloads)
        payload = json.dumps({'name': 'Basic', 'price': 85000, 'description': 'Basic oil changes and checks'})
        response = self.app.put('/servicepkg/api/v1/servicepkg/1', data=payload)
        self.assertEqual(response.status_code, 201)

    # tests updating a non existent sp fails
    def test_update_non_existence_sp(self):
        response = self.app.post('/servicepkg/api/v1/servicepkg', data=self.payloads)
        payload = json.dumps({'name': 'Enhanced'})
        response = self.app.put('/servicepkg/api/v1/servicepkg/3', data=payload)
        self.assertTrue(response.status_code == 404)

    # tests deleting a sp type
    def test_delete_sp(self):
        response = self.app.post('/servicepkg/api/v1/servicepkg', data=self.payloads)
        response = self.app.delete('/servicepkg/api/v1/servicepkg/1', data=self.payloads)
        self.assertTrue(response.status_code, 200)

    # tests deleting a non existent sp fails
    def test_delete_non_existence_sp(self):
        response = self.app.post('/servicepkg/api/v1/servicepkg', data=self.payloads)
        response = self.app.delete('/servicepkg/api/v1/servicepkg/3', data=self.payloads)
        self.assertTrue(response.status_code, 404)

    # tests that a pagination default is 3
    def test_get_pagination_default(self):
        response = self.app.get('/servicepkg/api/v1/servicepkg?limit=3')
        self.assertEqual(response.status_code, 200) 

    # tests search sp type by name
    def test_search_sp(self):
        response = self.app.post('/servicepkg/api/v1/servicepkg', data=self.payloads)
        response = self.app.get('/servicepkg/api/v1/servicepkg?q=Standard')
        self.assertEqual(response.status_code, 200)

    # tests search sp by name
    def test_search_non_existent_sp(self):
        response = self.app.post('/servicepkg/api/v1/servicepkg', data=self.payloads)
        response = self.app.get('/servicepkg/api/v1/servicepkg?q=Justbasic')
        self.assertIn('The service package you searched does not exist', response.data.decode('utf-8'))
