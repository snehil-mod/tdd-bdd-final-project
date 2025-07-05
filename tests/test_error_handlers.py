import unittest
from service import app
from service.common import status


class TestErrorHandlers(unittest.TestCase):
    """Test the custom error handlers"""

    def setUp(self):
        self.client = app.test_client()

    def test_404_not_found(self):
        """It should return a 404 Not Found error"""
        response = self.client.get("/nonexistent")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Not Found", response.get_json()["error"])

    def test_405_method_not_allowed(self):
        """It should return a 405 Method Not Allowed error"""
        response = self.client.put("/")  # PUT not allowed on homepage
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertIn("Method not Allowed", response.get_json()["error"])

    def test_500_internal_server_error(self):
        """It should return a 500 Internal Server Error"""
        response = self.client.get("/force-error")  # already defined in routes.py
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("Internal Server Error", response.get_json()["error"])
