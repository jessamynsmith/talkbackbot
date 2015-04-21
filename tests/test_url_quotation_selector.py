from mock import MagicMock, patch
import types
import unittest

from talkback.url_quotation_selector import UrlQuotationSelector


class TestUrlQuotationSelector(unittest.TestCase):

    def setUp(self):
        settings = types.ModuleType('test_url_settings')
        settings.QUOTES_URL = "https://example.com/api/v2/quotations/?limit=1"
        self.selector = UrlQuotationSelector(settings)

    @patch('requests.get')
    def test_select_failure(self, mock_get):
        mock_get.return_value = MagicMock(status_code=500)

        quote = self.selector.select()

        mock_get.assert_called_once_with('https://example.com/api/v2/quotations/?limit=1')
        self.assertEqual(None, quote)

    @patch('requests.get')
    def test_select_response_not_json(self, mock_get):
        mock_json = MagicMock(side_effect=ValueError())
        mock_get.return_value = MagicMock(status_code=200, json=mock_json)

        quote = self.selector.select()

        mock_get.assert_called_once_with('https://example.com/api/v2/quotations/?limit=1')
        self.assertEqual(None, quote)

    @patch('requests.get')
    def test_select_invalid_response_format(self, mock_get):
        mock_json = MagicMock(return_value={'text': 'Hi!', 'author': 'An'})
        mock_get.return_value = MagicMock(status_code=200, json=mock_json)

        quote = self.selector.select()

        mock_get.assert_called_once_with('https://example.com/api/v2/quotations/?limit=1')
        self.assertEqual(None, quote)

    @patch('requests.get')
    def test_select_success(self, mock_get):
        mock_json = MagicMock(return_value={'results': [{'text': 'Hi!', 'author': 'An'}]})
        mock_get.return_value = MagicMock(status_code=200, json=mock_json)

        quote = self.selector.select()

        mock_get.assert_called_once_with('https://example.com/api/v2/quotations/?limit=1')
        self.assertEqual('Hi! ~ An', quote)
        self.assertEqual(str, type(quote))
