
postcode-api-wrapper
====================

[![PyPI version](https://badge.fury.io/py/postcodepy.svg)](http://badge.fury.io/py/postcodepy)

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

      access_key="..."
      access_secret="..."
      # get your access key and secret at https://api.postcode.nl
      
      from postcodepy import postcodepy 

      import sys
      """First and third are OK, the 2nd is not OK and raises an Exception
           the exception is written to stderr
      """
      api = postcodepy.API( environment='live', access_key=access_key, access_secret=access_secret)

      # exit program if one of these exceptions occurs
      fatals = ['PostcodeNl_Controller_Plugin_HttpBasicAuthentication_NotAuthorizedException',
                'PostcodeNl_Controller_Plugin_HttpBasicAuthentication_PasswordNotCorrectException' ]

      # 2nd and last should fail
      for pc in [ ('1071XX', 1), ('1077XX', 1), ('7514BP', 129), ('7514BP', 129, 'A'), ('7514BP', 129, 'B')]:
          try:
            retValue = api.get_postcodedata( *pc )
            # the raw resultvalue
            print retValue
            # The parsed result 
            print "\nresults for: ", pc
            for K in retValue.keys():
              try:
                print "%30s : %s" % (K, retValue[K] )
              except Exception, e:
                print "ERROR: ", K

          except postcodepy.PostcodeError, e:
            if e.exceptionId in fatals:
              print >>sys.stderr, "Exiting on fatal exception: %s [%s]" % (e.exceptionId, e.msg)
              sys.exit(2)
            else:
              print >>sys.stderr, "---------------------------"
              print >>sys.stderr, e
              print >>sys.stderr, pc
              print >>sys.stderr, e.exceptionId
              print >>sys.stderr, e.response_data

          
## Output

Running the script above will give you this output and the exception on stderr


       {u'province': u'Noord-Holland', u'city': u'Amsterdam', u'bagAddressableObjectId': u'0363010012073352', u'addressType': u'building', u'rdY': 485901, u'bagNumberDesignationId': u'0363200012073684', u'municipality': u'Amsterdam', u'rdX': 120816, u'longitude': 4.88538896, u'purposes': [u'assembly'], u'houseNumberAddition': u'', u'street': u'Museumstraat', u'postcode': u'1071XX', u'houseNumberAdditions': [u''], u'latitude': 52.35994439, u'surfaceArea': 38149, u'houseNumber': 1}

       results for:  ('1071XX', 1)
                      province : Noord-Holland
                          city : Amsterdam
        bagAddressableObjectId : 0363010012073352
                   addressType : building
                           rdY : 485901
        bagNumberDesignationId : 0363200012073684
                  municipality : Amsterdam
                           rdX : 120816
                     longitude : 4.88538896
                      purposes : [u'assembly']
           houseNumberAddition : 
                        street : Museumstraat
                      postcode : 1071XX
          houseNumberAdditions : [u'']
                      latitude : 52.35994439
                   surfaceArea : 38149
                   houseNumber : 1
       {u'province': u'Overijssel', u'city': u'Enschede', u'bagAddressableObjectId': u'0153010000345343', u'addressType': u'building', u'rdY': 472143, u'bagNumberDesignationId': u'0153200000345342', u'municipality': u'Enschede', u'rdX': 258149, u'longitude': 6.89701549, u'purposes': [u'industry'], u'houseNumberAddition': u'', u'street': u'Lasondersingel', u'postcode': u'7514BP', u'houseNumberAdditions': [u'', u'A'], u'latitude': 52.22770127, u'surfaceArea': 6700, u'houseNumber': 129}

       results for:  ('7514BP', 129)
                      province : Overijssel
                          city : Enschede
        bagAddressableObjectId : 0153010000345343
                   addressType : building
                           rdY : 472143
        bagNumberDesignationId : 0153200000345342
                  municipality : Enschede
                           rdX : 258149
                     longitude : 6.89701549
                      purposes : [u'industry']
           houseNumberAddition : 
                        street : Lasondersingel
                      postcode : 7514BP
          houseNumberAdditions : [u'', u'A']
                      latitude : 52.22770127
                   surfaceArea : 6700
                   houseNumber : 129
       {u'province': u'Overijssel', u'city': u'Enschede', u'bagAddressableObjectId': u'0153010000329929', u'addressType': u'building', u'rdY': 472143, u'bagNumberDesignationId': u'0153200000329928', u'municipality': u'Enschede', u'rdX': 258149, u'longitude': 6.89701549, u'purposes': [u'residency'], u'houseNumberAddition': u'A', u'street': u'Lasondersingel', u'postcode': u'7514BP', u'houseNumberAdditions': [u'', u'A'], u'latitude': 52.22770127, u'surfaceArea': 119, u'houseNumber': 129}

       results for:  ('7514BP', 129, 'A')
                      province : Overijssel
                          city : Enschede
        bagAddressableObjectId : 0153010000329929
                   addressType : building
                           rdY : 472143
        bagNumberDesignationId : 0153200000329928
                  municipality : Enschede
                           rdX : 258149
                     longitude : 6.89701549
                      purposes : [u'residency']
           houseNumberAddition : A
                        street : Lasondersingel
                      postcode : 7514BP
          houseNumberAdditions : [u'', u'A']
                      latitude : 52.22770127
                   surfaceArea : 119
                   houseNumber : 129

## The exception of the 2nd postcode and last

        ---------------------------
        Combination does not exist.
        ('1077XX', 1)
        PostcodeNl_Service_PostcodeAddress_AddressNotFoundException
        {u'exception': u'Combination does not exist.', u'exceptionId': u'PostcodeNl_Service_PostcodeAddress_AddressNotFoundException'}
        ---------------------------
        Invalid housenumber addition: 'None'
        ('7514BP', 129, 'B')
        ERRHouseNumberAdditionInvalid
        {'validHouseNumberAdditions': [u'', u'A'], 'exception': "Invalid housenumber addition: 'None'", 'exceptionId': 'ERRHouseNumberAdditionInvalid'}


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
          print json.dumps(retValue, indent=4)

      except postcodepy.PostcodeError as e:
          print >>sys.stderr, e, e.exceptionId, e.response_data

