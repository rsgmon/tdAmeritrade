import unittest
from source import tdCall, credentials


class TestGetQuote(unittest.TestCase):
    def test_get_quote(self):
        key = {
            "headers": {
                "Authorization": "Bearer " + credentials.access_token
            }
        }
        mock_symbol_list = [["SPY", "AGG"], ["A"]]
        mock_params = {
            "get_params": {
                "path": [
                    "marketdata",
                    "quotes"
                ],
            },
        }
