from django.test import TestCase, Client
from . import views


# Create your tests here.
class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    # this tests are simple, they will need to be changed
    def test_api_get(self):
        response = self.client.get('/api/')
        content = response.content.decode("utf-8")
        self.assertEqual(content,'Hello, nice GET')

    def test_api_post(self):
        response = self.client.post('/api/')
        content = response.content.decode("utf-8")
        self.assertEqual(content,'Hello, nice POST')