"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status

class CounterTest(TestCase):
    """Counter tests"""
    def setUp(self):
        self.client = app.test_client()

    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """Tests to update Counters"""
        #Creates a counter
        result = self.client.post('/counters/updateCounter')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        #Check that it returns successful and check the counter value
        oldValue = result.json['updateCounter']
        newValue = self.client.put('/counters/updateCounter')
        self.assertEqual(newValue.status_code, status.HTTP_200_OK)
        #if the oldValue is less than the newValue that means we updated successfully
        self.assertLess(oldValue,newValue.json['updateCounter'])

    def test_read_a_counter(self):
        """Test to read a counter"""
        #Creates a counter
        result = self.client.post('/counters/readCounter')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        oldValue = result.json['readCounter']
        newValue = self.client.get('/counters/readCounter')
        self.assertEqual(newValue.status_code, status.HTTP_200_OK)
        self.assertEqual(oldValue,newValue.json['readCounter'])

    def test_delete_a_counter(self):
        """Test to delete a counter"""
        #Create a counter
        result = self.client.post('/counters/deleteCounter')
        #Check that it was created successfully
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        #Delete the created counter
        deleteResult = self.client.delete('/counters/deleteCounter')
        #Check that there is no counter that exists
        self.assertEqual(deleteResult.status_code, status.HTTP_204_NO_CONTENT)
        #delete a counter that doesnt even exists
        notReal = self.client.delete('counters/fakeCounter')
        #check that it is not found
        self.assertEqual(notReal.status_code, status.HTTP_404_NOT_FOUND)
