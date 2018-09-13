# tdAmeritrade
Libraries to help develop applications that consume tdAmeritrade's API.

**Uses asynchronous libraries. Requires python 3.5 or higher.** 

## Contents
    Introduction
    Background
        TdAmeritrade API
        tdAmeritrade Libraray (this project)
    Quick Start
    Contributions
    Reference
         

## Introduction
Welcome. The purpose of this project it to provide a library of functions, classes, and modules to help you more to quickly develop applications that consume tdAmeritrade's API. 

This readme will explain some background and experience with tdAmeritrade's API, and then the background and use of this project.

## Background
### TDAmeritrade API
The best place to learn about the TDAmeritrade API is at the [TDAmeritrade Developer Site](https://developer.tdameritrade.com/). 

#### Our experience
The [TDAmeritrade Developer Site](https://developer.tdameritrade.com/) documents two application types. 

The first type is your own local application. So for example you want to get options data. Follow [Simple Auth for Local Apps](https://developer.tdameritrade.com/content/simple-auth-local-apps) to get your first access key. Once completed, you'll have an access key and a refresh key. Save the refresh key in a secure place. Then you can repeatedly get access keys using the refesh key.  

The second application type is where you are running a server for either your own or someone else's use. Depending on the use you may need to get approval from TD.

### tdAmeritrade Library (this project)
Initially this library was built for the first reason: we wanted to pull and analyze data from TD. So **currently** this library makes one assumption.

**YOU ALREADY HAVE AN ACCESS KEY.**

The are currently there are two active modules.

_tdCall.py_ is updated and tested. It contains a single class designed to get data.

_authServer.py_ is really just a duplicate from td's developer site. I left it in but not much use as is.  

## Quick Start
**NOTE: YOU MUST HAVE AN ACCESS KEY TO GET DATA FROM TDAmeritrade.**

Go to [Simple Auth for Local Apps](https://developer.tdameritrade.com/content/simple-auth-local-apps) to find out how to get a key.

This is the absolute simplest call. It will return a quote for SPY.
```
from tdAmeritrade import tdCall
td_call = tdCall.tdCall([your access key])
print(td_call.get_td_data())
```

From there you can make more interesting requests. The below will get weekly price history for the last 3 months and options data for Apple and Netflix.  
```
from tdAmeritrade import tdCall
td_call = tdCall.tdCall([your access key], symbols=["AAPL","NFLX"], config=[{"route": "h", "periodType": "month", "period": 3, "frequencyType": "daily"}, {"route";"o"})
print(td_call.get_td_data())
```


## Contributions
Accepting all contributions! You may notice that not all of TDAmeritrade's API routes are included. Well that's because we haven't had to use them so far. Build or update a route!

Or often the data comes in a messy nested glob. We have helper functions that handle the data once received and we want even add complete reports. Build one!

## Reference
Help on module tdCall:

NAME
    tdCall

CLASSES
    builtins.object
        tdCall

    class tdCall(builtins.object)
       Prepares arguments for making HTTP calls to TDAmeritrade API.
       Gets data from TDAmeritrade API.
       Processes the result from TDAmeritrade.
     
       Methods defined here:
     
       __init__(self, key, symbols='SPY', configs=None)
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
     
       flatten_response(self, list_of_lists_of_prices)
           Flattens the response to a single list of dicts.
           :param list_of_lists_of_dicts:
           :return: list_of_dicts
     
       get_configs(self)
           :return: prepared config object capable of completely setting up HTTP get arguments
     
       get_coroutines(self, configs, symbols)
            Using the ClientSession it creates a list of functions ready to be executed. Then using gather asynchronous calls are made using the list.
           :param configs: list
           :param symbols: list
           :return: coroutine functions
       get_symbol_lists(self, symbol_file_name)
           Given a file name will asynchronously parse a list of symbols into a list of lists of symbols with each member list being 10 symbols long. This function was created to allow making a get request for the 10 symbols, processing the results (for example saving locally), an then making another get request. This assists in the event there is an error in getting data, the entire list need not be retreived.
           :param symbol_file_name:
           :return: list of lists of symbols
     
       get_td_data(self)
           Wrapper to get TDAmeritrade Data
           :return: list
     
       historical_prices(self, session, symbol, get_params)
           :param session: obj
           :param symbol: list
           :param get_params: dict
           :return: func
     
       multi_quote(self, session, symbols, get_params)
           :param session: obj
           :param symbol: list
           :param get_params: dict
           :return: func
     
       options(self, session, get_params)
           :param session: obj
           :param get_params: dict
           :return: func
     
       set_parse_symbols(self, symbol_file_name)
           :param symbol_file_name: string
           :return: list of list
     
       set_single_config(self, raw_config)
           :param raw_config: dict The user provided configuration.
           :return: a single config object
     
       wrap_schedule(self, coroutines)
           Scheduler for making asynchronous calls.
           :param coroutines:
           :return: list_of_lists_dict

