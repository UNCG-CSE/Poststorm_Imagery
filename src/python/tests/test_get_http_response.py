from unittest import TestCase

from src.python.Poststorm_Imagery.collector.ResponseGetter import get_http_response


class TestGetHTTPResponse(TestCase):
    def test_generic_response(self):
        self.assertTrue(get_http_response('https://www.google.com/').status_code)
