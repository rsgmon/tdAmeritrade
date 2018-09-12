import unittest
from source import tdCall, credentials


class TesttdCallGetData(unittest.TestCase):
    def test_get_configs(self):
        td_call = tdCall.tdCall(credentials.access_token, symbols=['SPY', 'AGG'], configs=[{'route':'h', 'periodType': 'daily'}])
        config = td_call.get_configs()
        self.assertEqual(type(config), list)

    def test_get_quote(self):
        td_call = tdCall.tdCall(credentials.access_token, symbols=['SPY'],
                                configs=[{'route': 'q'}])
        config = td_call.get_configs()
        result = td_call.wrap_schedule(td_call.get_coroutines(config, td_call.symbols))
        self.assertEqual(result[0][0]['symbol'], 'SPY')

    def test_select_coroutines_hist_no_parameters(self):
        td_call = tdCall.tdCall(credentials.access_token, symbols=['SPY'],
                                configs=[{'route': 'h'}])
        config = td_call.get_configs()
        result = td_call.wrap_schedule(td_call.get_coroutines(config, td_call.symbols))
        self.assertEqual(result[0][0]['symbol'], 'SPY')

    def test_select_coroutines_opt_no_parameters(self):
        td_call = tdCall.tdCall(credentials.access_token, symbols=['SPY'],
                                configs=[{'route': 'o'}])
        config = td_call.get_configs()
        result = td_call.wrap_schedule(td_call.get_coroutines(config, td_call.symbols))
        self.assertEqual(result[0][0]['symbol'], 'SPY')

    def test_select_coroutines_hist_opt_no_parameters(self):
        td_call = tdCall.tdCall(credentials.access_token, symbols=['SPY'],
                                configs=[{'route': 'h'},{'route': 'o'}])
        config = td_call.get_configs()
        coroutines = td_call.get_coroutines(config, td_call.symbols)
        result = td_call.wrap_schedule(coroutines)
        self.assertEqual(len(result), 2)

    def test_select_coroutines_no_route(self):
        td_call = tdCall.tdCall(credentials.access_token, symbols=['SPY'],
                                configs=[{"other":"test"}])
        self.assertRaises(ValueError, td_call.get_configs)
        td_call = tdCall.tdCall(credentials.access_token, symbols=['SPY'],
                                configs=[{}])
        self.assertRaises(ValueError, td_call.get_configs)

    def test_get_td_data(self):
        td_call = tdCall.tdCall(credentials.access_token, symbols=['SPY'],
                                configs=[{'route': 'h'}, {'route': 'o'}])
        self.assertEqual(len(td_call.get_td_data()),2)