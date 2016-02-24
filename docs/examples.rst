Examples
--------

Get information by ``postcode``:
````````````````````````````````

.. code-block:: python

    import sys
    import os
    from postcodepy import API, PostcodeError
    # First and third are OK, the 2nd is not OK and raises an Exception
    # the exception is written to stderr
    
    api = API(environment='live',
              access_key=os.getenv("ACCESS_KEY"),
              access_secret=os.getenv("ACCESS_SECRET"))
    for pc in [('1071XX', 1),
               ('8422DH', 34, 'B'),
               ('1077XX', 1),
               ('7514BP', 129)]:
        try:
            retValue = api.get_postcodedata(*pc)
            # the raw resultvalue
            print("\n--- RAW: ----------------------")
            print(retValue)
            # The parsed result
            print("\n--- Formatted: ----------------")
            print("\nresults for: {}".format(pc))
            for K in retValue.keys():
                try:
                    print("{0:30s} : {1}".format(K, retValue[K]))
                except Exception as e:
                    print("ERROR: {} {}".format( (K, retValue[K])))
    
        except PostcodeError as e:
            sys.stdout.write("EXCEPTION:\n")
            sys.stdout.write("{0} {1} {2} {3}\n".
                             format(e, pc, e.exceptionId, e.response_data))


Output
``````

.. code-block:: text


    --- RAW: ----------------------
    {u'province': u'Noord-Holland', u'city': u'Amsterdam', u'bagAddressableObjectId': u'0363010012073352', u'addressType': u'building', u'rdY': 485901, u'bagNumberDesignationId': u'0363200012073684', u'municipality': u'Amsterdam', u'rdX': 120816, u'longitude': 4.88538896, u'purposes': [u'assembly'], u'houseNumberAddition': u'', u'street': u'Museumstraat', u'postcode': u'1071XX', u'houseNumberAdditions': [u''], u'latitude': 52.35994439, u'surfaceArea': 38149, u'houseNumber': 1}
    
    --- Formatted: ----------------
    
    results for: ('1071XX', 1)
    province                       : Noord-Holland
    city                           : Amsterdam
    bagAddressableObjectId         : 0363010012073352
    addressType                    : building
    rdY                            : 485901
    bagNumberDesignationId         : 0363200012073684
    municipality                   : Amsterdam
    rdX                            : 120816
    longitude                      : 4.88538896
    purposes                       : [u'assembly']
    houseNumberAddition            : 
    street                         : Museumstraat
    postcode                       : 1071XX
    houseNumberAdditions           : [u'']
    latitude                       : 52.35994439
    surfaceArea                    : 38149
    houseNumber                    : 1
    EXCEPTION:
    Invalid housenumber addition: 'None' ('8422DH', 34, 'B') ERRHouseNumberAdditionInvalid {'validHouseNumberAdditions': [u'', u'A'], 'exception': "Invalid housenumber addition: 'None'", 'exceptionId': 'ERRHouseNumberAdditionInvalid'}
    EXCEPTION:
    Combination does not exist. ('1077XX', 1) PostcodeNl_Service_PostcodeAddress_AddressNotFoundException {u'exception': u'Combination does not exist.', u'exceptionId': u'PostcodeNl_Service_PostcodeAddress_AddressNotFoundException'}
    
    --- RAW: ----------------------
    {u'province': u'Overijssel', u'city': u'Enschede', u'bagAddressableObjectId': u'0153010000345343', u'addressType': u'building', u'rdY': 472143, u'bagNumberDesignationId': u'0153200000345342', u'municipality': u'Enschede', u'rdX': 258149, u'longitude': 6.89701549, u'purposes': [u'assembly'], u'houseNumberAddition': u'', u'street': u'Lasondersingel', u'postcode': u'7514BP', u'houseNumberAdditions': [u'', u'A'], u'latitude': 52.22770127, u'surfaceArea': 6700, u'houseNumber': 129}
    
    --- Formatted: ----------------
    
    results for: ('7514BP', 129)
    province                       : Overijssel
    city                           : Enschede
    bagAddressableObjectId         : 0153010000345343
    addressType                    : building
    rdY                            : 472143
    bagNumberDesignationId         : 0153200000345342
    municipality                   : Enschede
    rdX                            : 258149
    longitude                      : 6.89701549
    purposes                       : [u'assembly']
    houseNumberAddition            : 
    street                         : Lasondersingel
    postcode                       : 7514BP
    houseNumberAdditions           : [u'', u'A']
    latitude                       : 52.22770127
    surfaceArea                    : 6700
    houseNumber                    : 129
