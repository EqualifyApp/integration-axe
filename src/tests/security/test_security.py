import unittest
from flask import session
from app import app


class TestSecurity(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_session_cookie_httponly(self):
        response = self.app.get('/')
        self.assertIn('HttpOnly', response.headers['Set-Cookie'])

    def test_session_cookie_secure(self):
        response = self.app.get('/')
        self.assertIn('Secure', response.headers['Set-Cookie'])

    def test_xss_protection_header(self):
        response = self.app.get('/')
        self.assertIn('X-XSS-Protection', response.headers)
        self.assertEqual(response.headers['X-XSS-Protection'], '1; mode=block')

    def test_content_security_policy_header(self):
        response = self.app.get('/')
        self.assertIn('Content-Security-Policy', response.headers)
        self.assertEqual(response.headers['Content-Security-Policy'], "default-src 'self'")

    def test_x_content_type_options_header(self):
        response = self.app.get('/')
        self.assertIn('X-Content-Type-Options', response.headers)
        self.assertEqual(response.headers['X-Content-Type-Options'], 'nosniff')


if __name__ == '__main__':
    unittest.main()
