import unittest
import json
from app import app


class TestIntegration(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_axe_scan(self):
        url = 'https://www.google.com'
        response = self.app.get(f'/axe?url={url}')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('scanned_at', response_data)
        self.assertIn('url', response_data)
        self.assertEqual(response_data['url'], url)


if __name__ == '__main__':
    unittest.main()
