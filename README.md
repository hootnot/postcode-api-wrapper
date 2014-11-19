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
      
      
      from postcodepy.postcodepy import API, PostcodeError
      
      import sys
      """First and third are OK, the 2nd is not OK and raises an Exception
           the exception is written to stderr
      """
      api = API( environment='live', access_key=access_key, access_secret=access_secret)
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
              print "ERROR: ", K, retValue[K]
      
        except PostcodeError, e:
          print >>sys.stderr, e, pc
          
