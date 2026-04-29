"""Unit tests for the HTTP server in manage.py"""
import unittest
from io import BytesIO
from unittest.mock import patch, MagicMock

# Import from manage.py (server won't start thanks to __name__ guard)
from manage import MyHandler, PORT, Handler


class TestHTTPServer(unittest.TestCase):
    """Test cases for the custom HTTP server handler"""

    def _make_handler(self):
        """Create a handler with mocked socket setup"""
        with patch.object(MyHandler, 'setup', lambda self: None):
            with patch.object(MyHandler, 'handle', lambda self: None):
                with patch.object(MyHandler, 'finish', lambda self: None):
                    handler = MyHandler(
                        request=MagicMock(),
                        client_address=('127.0.0.1', 12345),
                        server=None
                    )
        handler.wfile = BytesIO()
        handler.rfile = BytesIO()
        return handler

    def test_handler_get_response_status(self):
        """Test that GET request returns 200 status and text/html header"""
        handler = self._make_handler()

        status_captured = {}
        headers_captured = {}

        def mock_send_response(code, message=None):
            status_captured['code'] = code

        def mock_send_header(keyword, value):
            headers_captured[keyword] = value

        # Patch methods
        handler.send_response = mock_send_response
        handler.send_header = mock_send_header
        handler.end_headers = lambda: None

        handler.do_GET()

        self.assertEqual(status_captured.get('code'), 200)
        self.assertIn("Content-type", headers_captured)
        self.assertEqual(headers_captured["Content-type"], "text/html")

    def test_handler_response_content(self):
        """Test that response contains expected HTML content"""
        handler = self._make_handler()

        handler.send_response = lambda x: None
        handler.send_header = lambda k, v: None
        handler.end_headers = lambda: None

        handler.do_GET()

        response_body = handler.wfile.getvalue().decode('utf-8')

        # Check for expected content
        self.assertIn("Jenkins-K8s Pipeline Successful", response_body)
        self.assertIn("Pod is Running", response_body)
        self.assertIn("TGPCET Nagpur", response_body)
        self.assertIn("<html>", response_body)
        self.assertIn("</html>", response_body)


class TestServerStartup(unittest.TestCase):
    """Test server startup and configuration"""

    def test_port_constant(self):
        """Test that PORT is set to 8000"""
        self.assertEqual(PORT, 8000)

    def test_handler_class_exists(self):
        """Test that MyHandler class is defined and callable"""
        self.assertTrue(callable(MyHandler))

    def test_handler_alias(self):
        """Test that Handler alias points to MyHandler"""
        self.assertIs(Handler, MyHandler)


if __name__ == '__main__':
    unittest.main()

