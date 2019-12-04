from unittest import TestCase

import requests

from psicollect.collector.response_getter import get_http_response, get_full_content_length


class TestResponseGetter(TestCase):

    def test_generic_response_success(self):
        self.assertEqual(requests.codes.ok, get_http_response('https://www.google.com/').status_code)

    def test_generic_response_failed(self):
        with self.assertRaises(ConnectionError):
            get_http_response('http://www.google.com/thispagedoesnotexist')

    def test_generic_response_exception(self):
        with self.assertRaises(ConnectionError):
            get_http_response('http:///')

    def test_get_full_content_length_correct(self):
        self.assertEqual(11397775360, get_full_content_length(
            'https://ngsstormviewer.blob.core.windows.net/downloads/20180915a_jpgs.tar'))

    def test_get_full_content_length_empty(self):
        self.assertEqual(0, get_full_content_length('https://httpbin.org/status/404'))
