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
Welcome. The purpose of this repository it to provide a library of functions, classes, and modules to help you more to quickly develop applications that consume tdAmeritrade's API. 

This readme will explain some background and experience with tdAmeritrade's API, and then the background and use of this project.

## Background
### TDAmeritrade API
The best place to learn about the TDAmeritrade API is at the [TDAmeritrade Developer Site](https://developer.tdameritrade.com/). 

#### Our experience
The [TDAmeritrade Developer Site](https://developer.tdameritrade.com/) documents two application types. 

The first type is your own local application. So for example you want to options data. Follow [Simple Auth for Local Apps](https://developer.tdameritrade.com/content/simple-auth-local-apps) to get your first access key. Once completed, you'll have an access key and a refresh key. Save the refresh key in a secure place. Then you can repeatedly get access keys using the refesh key.  

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

from tdAmeritrade import tdCall
td_call = tdCall.tdCall([your access key])
print(td_call.get_td_data())


## Contributions










## Current Status
trd

