import asyncio
import aiohttp
import async_timeout
import copy

class tdCall(object):
    """
    Prepares arguments for making HTTP calls to TDAmeritrade API.
    Gets data from TDAmeritrade API.
    Processes the result from TDAmeritrade.
    """
    base_url = "https://api.tdameritrade.com/v1/"
    def __init__(self, key, symbols="SPY", configs=None):
        """
        :param key: string TDAmeritrade Access Key
        :param symbols: string or list, Stock Symbols
        :param configs: dict or list of dicts,
            required:
                route: string
                    "q" : qoutes endpoint
                    "h" : price history endpoint
                    "o" : options endpoint
            optional:
                Each endpoint has different parameters. See TDAmeritrade's developer website.

            Examples:
                This will get daily historical prices for the last three months.
                {"route": "h", "periodType": "month", "period": 3, "frequencyType": "daily"}

                This will get vertical spreads for just calls, within one strike from at the money.
                {"route": "o", "contractType": "CALL", "strikeCount": 3, "strategy": "VERTICAL"}

                This will get quotes and options with all other arguments using the api's default.
                [{"route": "q"}, {"route": "o"}]
        """
        self.key = key
        self.raw_configs = configs
        if isinstance(symbols, str):
            self.symbols = [symbols]
        else: self.symbols = symbols

    def get_configs(self):
        """

        :return: prepared config object capable of completely setting up HTTP get arguments
        """
        if not self.raw_configs:
            return [self.quotes]
        else:
            if len(self.raw_configs) == 1 and isinstance(self.raw_configs, dict):
                return [self.set_single_config(self.raw_configs)]
            else:
                refined_configs = []
                for config in self.raw_configs:
                    refined_configs.append(self.set_single_config(config))
                return refined_configs

    def set_single_config(self, raw_config):
        """

        :param raw_config: dict The user provided configuration.
        :return: a single config object
        """
        if not raw_config:
            raise ValueError("Your configuration was empty. You don't have to include a configuration but if you do it must contain values.")
        elif 'route' not in raw_config.keys():
            raise ValueError('You specified a configuration without a route. All configurations must include a route.')
        elif raw_config['route'] == 'h':
            static_config = self.hist
        elif raw_config['route'] == 'o':
            static_config = self.opts
        else:
            static_config = self.quotes
        for index, value in raw_config.items():
            if index == 'route': continue
            static_config['get_params']['param_vars'][index] = value
        return static_config

    def get_symbol_lists(self, symbol_file_name):
        """
        Given a file name will asynchronously parse a list of symbols into a list of lists of symbols with each member list being 10 symbols long. This function was created to allow making a get request for the 10 symbols, processing the results (for example saving locally), an then making another get request. This assists in the event there is an error in getting data, the entire list need not be retreived.
        :param symbol_file_name:
        :return: list of lists of symbols
        """
        coroutine = self.set_parse_symbols(symbol_file_name)
        symbols = self.wrap_schedule(coroutine)
        return symbols

    async def get_coroutines(self, configs, symbols):
        """
         Using the ClientSession it creates a list of functions ready to be executed. Then using gather asynchronous calls are made using the list.
        :param configs: list
        :param symbols: list
        :return: coroutine functions
        """
        async with aiohttp.ClientSession() as session:
            all_calls = []
            for config in configs:
                tasks = []
                if config['func'] == 'test':
                    return 1
                if config['func'] == 'options':
                    for item in symbols:
                        config['get_params']['param_vars']['symbol'] = item
                        tasks.append(self.options(session, copy.deepcopy(config['get_params'])))
                elif config['func'] == 'multi_quote':
                    """.join turns the list into str separated by commas.
                     This is necessary to be able to make a get call with multiple Strings"""
                    tasks.append(self.multi_quote(session, ','.join(symbols), config['get_params']))
                else:
                    tasks = [self.historical_prices(session, item, config['get_params']) for item in symbols]
                single_endpoint = await asyncio.gather(*tasks)
                all_calls.append(single_endpoint)
            return all_calls

    async def historical_prices(self, session, symbol, get_params):
        """
        :param session: obj
        :param symbol: list
        :param get_params: dict
        :return: func
        """
        """Only works as part of the the get_data function. It essentially sets everything up for an http call."""
        with async_timeout.timeout(100):
            async with session.get(self.base_url + get_params['path'][0] + "/" + symbol + "/" + get_params['path'][1],
                                   headers=get_params['headers'], params=get_params['param_vars']) as response:
                return await response.json()

    async def options(self, session, get_params):
        """
        :param session: obj
        :param get_params: dict
        :return: func
        """
        with async_timeout.timeout(100):
            async with session.get(self.base_url + get_params['path'][0] + "/" + get_params['path'][1],
                                   headers=get_params['headers'], params=get_params['param_vars']) as response:
                return await response.json()

    async def multi_quote(self, session, symbols, get_params):
        """
        :param session: obj
        :param symbol: list
        :param get_params: dict
        :return: func
        """
        with async_timeout.timeout(100):
            async with session.get(self.base_url + get_params['path'][0] + "/" + get_params['path'][1],
                                   headers=get_params['headers'], params={'symbol': symbols}) as response:
                return await response.json()

    def get_td_data(self):
        """
        Wrapper to get TDAmeritrade Data
        :return: list
        """
        configurations = self.get_configs()
        coroutines = self.get_coroutines(configurations, self.symbols)
        return self.wrap_schedule(coroutines)

    def flatten_response(self, list_of_lists_of_prices):
        """
        Flattens the response to a single list of dicts.
        :param list_of_lists_of_dicts:
        :return: list_of_dicts
        """
        result = []
        for list_of_list_of_prices in list_of_lists_of_prices:
            [result.append(p) for p in list_of_list_of_prices]
        return result

    def wrap_schedule(self, coroutines):
        """
        Scheduler for making asynchronous calls.
        :param coroutines:
        :return: list_of_lists_dict
        """
        loop = asyncio.get_event_loop()
        task = asyncio.ensure_future(coroutines)
        return loop.run_until_complete(task)

    async def set_parse_symbols(self, symbol_file_name):
        """

        :param symbol_file_name: string
        :return: list of list
        """
        with open(symbol_file_name, 'r') as file:
            symbols = []
            for l in file:
                parsed_line = await self._parse_line(l)
                # for group in parsed_line:
                #     que = await get_data(group, symbol_file_name)
                if all(isinstance(elem, list) for elem in parsed_line):
                    for p in parsed_line:
                        symbols.append(p)
                else:
                    symbols.append(parsed_line)
        return symbols

    async def _parse_line(self, line):
        """

        :param line:
        :return: list
        """
        parsed_line = "[" + line[:-1] + "]"
        if len(parsed_line) > 10:
            queue = [parsed_line[i:i + 10] for i in range(0, len(parsed_line), 10)]
        else:
            queue = parsed_line
        await asyncio.sleep(0)
        return queue

    _historical = {
        "get_params": {
            "param_vars": {},
            "path": [
                "marketdata",
                "pricehistory"
            ],
            "headers": {
                "Authorization": None
            }
        },
        "func": "historical_prices"
    }

    @property
    def hist(self):
        self._historical['get_params']['headers']['Authorization'] = "Bearer " + self.key
        return self._historical

    _quotes = {
        "get_params": {
            "param_vars": {},
            "path": [
                "marketdata",
                "quotes"
            ],
            "headers": {
                "Authorization": None
            }
        },
        "func": "multi_quote"
    }

    @property
    def quotes(self):
        self._quotes['get_params']['headers']['Authorization'] = "Bearer " + self.key
        return self._quotes

    _options = {
        "func": "options",
        "get_params":
            {
                "param_vars": {},
                "path": [
                    "marketdata",
                    "chains"
                ],
                "headers": {"Authorization": None}
            }
    }

    @property
    def opts(self):
        self._options['get_params']['headers']['Authorization'] = "Bearer " + self.key
        return self._options