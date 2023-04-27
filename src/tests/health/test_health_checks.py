import unittest
from app import app


class TestHealthChecks(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'UP'})


if __name__ == '__main__':
    unittest.main()
