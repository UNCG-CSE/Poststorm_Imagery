from unittest import TestCase

import requests

from src.python.Poststorm_Imagery.collector.ResponseGetter import get_http_response, get_full_content_length


class TestResponseGetter(TestCase):

    def test_generic_response_success(self):
        self.assertEqual(requests.codes.ok, get_http_response('https://www.google.com/').status_code)

    def test_generic_response_failed(self):
        with self.assertRaises(SystemExit):
            get_http_response('http://google.com/thispagedoesnotexist')

    def test_get_full_content_length_correct(self):
        self.assertEqual(11397775360, get_full_content_length(
            'https://ngsstormviewer.blob.core.windows.net/downloads/20180915a_jpgs.tar'))
