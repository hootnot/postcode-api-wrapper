postcode-api-wrapper
====================

API Wrapper for the API of Postcode.nl

Install
========
This module is also installable using **pip**

        $ sudo pip install postcodepy


About
==========

This module is handy to be used in web applications to autocomplete address information.

As it comes, it is specific for the Netherlands. So in Dutch:

## ... in Dutch ...
Deze module is handig om in web-applicaties te gebruiken om op basis van postcode en huisnummer eenvoudig complete adres informatie op te kunnen vragen.

De API van postcode.nl wordt hiervoor gebruikt. Op [https://api.postcode.nl](https://api.postcode.nl) kunt u zich registreren voor het gebruik van deze API en daarmee de beschikking krijgen over een 'secret' en een 'key' die benodigd zijn om deze API te kunnen gebruiken.

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
      for pc in [ ('1071XX', 1), ('1077XX', 1), ('7514BP', 129) ]:
          try:
            retValue = api.get_postcodedata( pc[0], pc[1] )
            # the raw resultvalue
            print retValue
            # The parsed result 
            print "\nresults for: ", pc[0], pc[1]
            for K in retValue.keys():
              try:
                print "%30s : %s" % (K, retValue[K] )
              except Exception, e:
                print "ERROR: ", K

          except postcodepy.PostcodeError, e:
            print >>sys.stderr, e
            print >>sys.stderr, pc
            print >>sys.stderr, e.response_data
          
## Output

Running the script above will give you this output and the exception on stderr

       {u'province': u'Noord-Holland', u'city': u'Amsterdam', u'bagAddressableObjectId': u'0363010012073352', u'addressType': u'building', u'rdY': 485901, u'bagNumberDesignationId': u'0363200012073684', u'municipality': u'Amsterdam', u'rdX': 120816, u'longitude': 4.8853889600000002, u'purposes': [u'assembly'], u'houseNumberAddition': u'', u'street': u'Museumstraat', u'postcode': u'1071XX', u'houseNumberAdditions': [u''], u'latitude': 52.359944390000003, u'surfaceArea': 38149, u'houseNumber': 1}

       results for:  1071XX 1
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
       {u'province': u'Overijssel', u'city': u'Enschede', u'bagAddressableObjectId': u'0153010000345343', u'addressType': u'building', u'rdY': 472143, u'bagNumberDesignationId': u'0153200000345342', u'municipality': u'Enschede', u'rdX': 258149, u'longitude': 6.8970154900000002, u'purposes': [u'industry'], u'houseNumberAddition': u'', u'street': u'Lasondersingel', u'postcode': u'7514BP', u'houseNumberAdditions': [u'', u'A'], u'latitude': 52.227701269999997, u'surfaceArea': 6700, u'houseNumber': 129}

       results for:  7514BP 129
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

## The exception of the 2nd postcode


      EXCEPTION: APIServerERRuserInputError (User Input Error) ID: PostcodeNl_Service_PostcodeAddress_AddressNotFoundException Description: Combination does not exist.
      ('1077XX', 1)
      {u'exception': u'Combination does not exist.', u'exceptionId': u'PostcodeNl_Service_PostcodeAddress_AddressNotFoundException'}
