from django.test import TestCase, Client
from . import views


# Create your tests here.
class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()



    def test_api_post(self):
        response = self.client.post('/api/action/', {"example" : "example"})
        content = response.content.decode("utf-8")
        self.assertEqual(content,'Hello, nice POST')