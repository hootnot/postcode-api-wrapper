
postcode-api-wrapper
====================

[![Build Status](https://travis-ci.org/hootnot/postcode-api-wrapper.svg?branch=master)](https://travis-ci.org/hootnot/postcode-api-wrapper)
[![Documentation Status](http://readthedocs.org/projects/postcode-api-wrapper/badge/?version=latest)](http://postcode-api-wrapper.readthedocs.org/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/postcodepy.svg)](http://badge.fury.io/py/postcodepy)
[![Code Health](https://landscape.io/github/hootnot/postcode-api-wrapper/master/landscape.svg?style=flat)](https://landscape.io/github/hootnot/postcode-api-wrapper/master)
[![Coverage Status](https://coveralls.io/repos/github/hootnot/postcode-api-wrapper/badge.svg?branch=master)](https://coveralls.io/github/hootnot/postcode-api-wrapper?branch=master)

API Wrapper for the API of Postcode.nl

---

Install
========
This module is also installable using **pip**

        $ sudo pip install postcodepy


About
==========

This module is handy to be used in web applications to autocomplete address information. There is also an
endpoint for information validation, enrichment and fraud risk check. See the docs for details.

As it comes, it is specific for the Netherlands. So in Dutch:

## ... in Dutch ...
Deze module is handig om in web-applicaties te gebruiken om op basis van postcode en huisnummer eenvoudig complete adres informatie op te kunnen vragen.

De API van postcode.nl wordt hiervoor gebruikt. Op [https://api.postcode.nl](https://api.postcode.nl) kunt u zich registreren voor het gebruik van deze API en daarmee de beschikking krijgen over een 'secret' en een 'key' die benodigd zijn om deze API te kunnen gebruiken.

De Signaal-API kan worden gebruikt voor validatie, controle en verrijking van transactie- en klantgegevens.

Authentication
==============
If you want to use this module or you want to run the tests you *need* to have
an **access_key** and a **access_secret**. 

Example
===========

    import os
    import sys
    import json
    import postcodepy

    access_key = os.getenv("ACCESS_KEY")
    access_secret = os.getenv("ACCESS_SECRET")
    # get your access key and secret at https://api.postcode.nl

    """First and third are OK, the 2nd is not OK and raises an Exception
         the exception is written to stderr
    """
    api = postcodepy.API(environment='live',
                         access_key=access_key, access_secret=access_secret)

    # exit program if one of these exceptions occurs
    fatals = [
        'PostcodeNl_Controller_Plugin_HttpBasicAuthentication_NotAuthorizedException',
        'PostcodeNl_Controller_Plugin_HttpBasicAuthentication_PasswordNotCorrectException'
    ]

    # 2nd and last should fail
    for pc in [('1071XX', 1),
               ('1077XX', 1),
               ('7514BP', 129),
               ('7514BP', 129, 'A'),
               ('7514BP', 129, 'B')]:
        try:
            retValue = api.get_postcodedata(*pc)
            print("\nresults for: {}".format(str(pc)))
            print(json.dumps(retValue, sort_keys=True, indent=2))

        except postcodepy.PostcodeError as e:
            if e.exceptionId in fatals:
                sys.stderr.write("Exiting on fatal exception: {} [{}]".
                                 format(e.exceptionId, e.msg))
                sys.exit(2)
            else:
                sys.stderr.write("---------------------------\n")
                sys.stderr.write("{}\n".format(str(pc)))
                sys.stderr.write("{}\n".format(e.exceptionId))
                sys.stderr.write("{}\n".format(json.dumps(
                      e.response_data, sort_keys=True, indent=2))
                )

## Output

Running the script above will give you this JSON output and the exception on stderr

    results for: ('1071XX', 1)
    {
      "addressType": "building", 
      "bagAddressableObjectId": "0363010012073352", 
      "bagNumberDesignationId": "0363200012073684", 
      "city": "Amsterdam", 
      "houseNumber": 1, 
      "houseNumberAddition": "", 
      "houseNumberAdditions": [
        ""
      ], 
      "latitude": 52.35994439, 
      "longitude": 4.88538896, 
      "municipality": "Amsterdam", 
      "postcode": "1071XX", 
      "province": "Noord-Holland", 
      "purposes": [
        "assembly"
      ], 
      "rdX": 120816, 
      "rdY": 485901, 
      "street": "Museumstraat", 
      "surfaceArea": 38149
    }
    
    results for: ('7514BP', 129)
    {
      "addressType": "building", 
      "bagAddressableObjectId": "0153010000345343", 
      "bagNumberDesignationId": "0153200000345342", 
      "city": "Enschede", 
      "houseNumber": 129, 
      "houseNumberAddition": "", 
      "houseNumberAdditions": [
        "", 
        "A"
      ], 
      "latitude": 52.22770127, 
      "longitude": 6.89701549, 
      "municipality": "Enschede", 
      "postcode": "7514BP", 
      "province": "Overijssel", 
      "purposes": [
        "assembly"
      ], 
      "rdX": 258149, 
      "rdY": 472143, 
      "street": "Lasondersingel", 
      "surfaceArea": 6700
    }
    
    results for: ('7514BP', 129, 'A')
    {
      "addressType": "building", 
      "bagAddressableObjectId": "0153010000329929", 
      "bagNumberDesignationId": "0153200000329928", 
      "city": "Enschede", 
      "houseNumber": 129, 
      "houseNumberAddition": "A", 
      "houseNumberAdditions": [
        "", 
        "A"
      ], 
      "latitude": 52.22770127, 
      "longitude": 6.89701549, 
      "municipality": "Enschede", 
      "postcode": "7514BP", 
      "province": "Overijssel", 
      "purposes": [
        "residency"
      ], 
      "rdX": 258149, 
      "rdY": 472143, 
      "street": "Lasondersingel", 
      "surfaceArea": 119
    }

## The exception of the 2nd postcode and last

    ---------------------------
    ('1077XX', 1)
    PostcodeNl_Service_PostcodeAddress_AddressNotFoundException
    {
      "exception": "Combination does not exist.", 
      "exceptionId": "PostcodeNl_Service_PostcodeAddress_AddressNotFoundException"
    }
    ---------------------------
    ('7514BP', 129, 'B')
    ERRHouseNumberAdditionInvalid
    {
      "exception": "Invalid housenumber addition: 'None'", 
      "exceptionId": "ERRHouseNumberAdditionInvalid", 
      "validHouseNumberAdditions": [
        "", 
        "A"
      ]
    }


Signal API example
==================

      access_key="..."
      access_secret="..."
      # get your access key and secret at https://api.postcode.nl
      
      from postcodepy import postcodepy 

      import os, sys
      import json

      """ TEST: signal check URL, a request that should report 1 warning, with 6 signals
      """
      api = postcodepy.API( environment='live', access_key=access_key, access_secret=access_secret)

      retValue = None
      try:
          dct = { "customer": {
                                   "email": "test-address@postcode.nl",
                             "phoneNumber": "+31235325689",
                                 "address": {
                                                "postcode": "2012ES",
                                             "houseNumber": "30",
                                                 "country": "NL"
                                            }
                              },
               "transaction": {
                              "internalId": "MyID-249084",
                         "deliveryAddress": {
                                             "postcode": "2012ES",
                                          "houseNumber": "99",
                                              "country": "NL"
                                            }
                              }
                 }
          
          retValue = api.get_signalcheck( dct )
          print(json.dumps(retValue, indent=4))

      except postcodepy.PostcodeError as e:
          sys.stderr.write("{}, {}, {}".format(e, e.exceptionId,
                                               json.dumps(e.response_data, sort_keys=True, indent=2))
