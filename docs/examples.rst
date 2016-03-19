Examples
--------

Get information by ``postcode``:
````````````````````````````````

.. code-block:: python

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

Output
``````

.. code-block:: text

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

Exceptions
~~~~~~~~~~

.. code-block:: text

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
