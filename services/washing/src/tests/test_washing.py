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


# tests all functionality of washing.py and there defined methods
class WashingTestCases(unittest.TestCase):
    # testing client using testing environment
    def setUp(self):
        self.app = app.test_client()
        EnvironmentName('TestingEnvironment')
        databases.create_all()

        # creating a washing type for testing purpose
        self.payloads = json.dumps({'name': 'Basic', 'price': 7000, 'description': 'basic body wash'})

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    # tests that a washing model is successfully created
    def test_create_new_washing_package(self):
        response = self.app.post('/washing/api/v1/washingtypes', data=self.payloads)
        self.assertTrue(response.status_code == 201)
        self.assertIn('Washing package added successfully', response.data.decode('utf-8'))

    # tests creation of wash model fails without name
    def test_create_new_washing_without_name(self):
        payload = json.dumps({'name': ''})
        response = self.app.post('/washing/api/v1/washingtypes', data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('washing package has no name', response.data.decode('utf-8'))

    # tests creation of wash model fails without price
    def test_create_new_washing_without_price(self):
        payload = json.dumps({'price': '', 'name': 'valuehere'})
        response = self.app.post('/washing/api/v1/washingtypes', data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('washing package has no price tag', response.data.decode('utf-8'))

    # tests creation of wash model fails without name
    def test_create_new_washing_without_description(self):
        payload = json.dumps({'description': '', 'price': 45, 'name': 'valuehere'})
        response = self.app.post('/washing/api/v1/washingtypes', data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('washing package has no description', response.data.decode('utf-8'))

    # tests creation of washing fails with existing name
    def test_create_existing_washing_model(self):
        response = self.app.post('/washing/api/v1/washingtypes', data=self.payloads)
        response = self.app.post('/washing/api/v1/washingtypes', data=self.payloads)
        self.assertEqual(response.status_code, 409)

    # tests that a wash successfully created is retrieved
    def test_get_washing_type(self):
        response = self.app.post('/washing/api/v1/washingtypes', data=self.payloads)
        response = self.app.get('/washing/api/v1/washingtypes')
        self.assertEqual(response.status_code, 200)

    # tests that a washing not successfully created is not found
    def test_get_washing_while_database_empty(self):
        response = self.app.get('/washing/api/v1/washingtypes')
        self.assertTrue(response.status_code == 200)
        self.assertIn('No washing package has been created yet', response.data.decode('utf-8'))  #

    # tests getting a washing type by id
    def test_get_wash_by_id(self):
        response = self.app.post('/washing/api/v1/washingtypes', data=self.payloads)
        response = self.app.get('/washing/api/v1/washingtypes/1')
        self.assertEqual(response.status_code, 200)

    # tests getting a wash by invalid id fails
    def test_get_wash_by_invalid_id(self):
        response = self.app.post('/washing/api/v1/washingtypes', data=self.payloads)
        response = self.app.get('/washing/api/v1/washingtypes/8')
        self.assertEqual(response.status_code, 404)

    # tests updating a washing
    def test_update_washing(self):
        response = self.app.post('/washing/api/v1/washingtypes', data=self.payloads)
        payload = json.dumps({'name': 'Standard', 'price': 12000, 'description': 'body wash, interior cleaning and thourough tyres brushing'})
        response = self.app.put('/washing/api/v1/washingtypes/1', data=payload)
        self.assertEqual(response.status_code, 201)

    # tests updating a non existent washing fails
    def test_update_non_existence_washing(self):
        response = self.app.post('/washing/api/v1/washingtypes', data=self.payloads)
        payload = json.dumps({'name': 'Enhanced'})
        response = self.app.put('/washing/api/v1/washingtype/3', data=payload)
        self.assertTrue(response.status_code == 404)

    # tests deleting a washing type
    def test_delete_washing(self):
        response = self.app.post('/washing/api/v1/washingtypes', data=self.payloads)
        response = self.app.delete('/washing/api/v1/washingtypes/1', data=self.payloads)
        self.assertTrue(response.status_code, 200)

    # tests deleting a non existent washing fails
    def test_delete_non_existence_washing(self):
        response = self.app.post('/washing/api/v1/washingtypes', data=self.payloads)
        response = self.app.delete('/washing/api/v1/washingtypes/3', data=self.payloads)
        self.assertTrue(response.status_code, 404)

    # tests that a pagination default is 3
    def test_get_pagination_default(self):
        response = self.app.get('/washing/api/v1/washingtypes?limit=3')
        self.assertEqual(response.status_code, 200) 

    # tests search washing type by name
    def test_search_washing(self):
        response = self.app.post('washing/api/v1/washingtypes', data=self.payloads)
        response = self.app.get('/washing/api/v1/washingtypes?q=Basic')
        self.assertEqual(response.status_code, 200)

    # tests search wash by name
    def test_search_non_existent_washing(self):
        response = self.app.post('/washing/api/v1/washingtypes', data=self.payloads)
        response = self.app.get('/washing/api/v1/washingtypes?q=Shit')
        # self.assertEqual(response.status_code, 404)
        self.assertIn('The washing package you searched does not exist', response.data.decode('utf-8'))
