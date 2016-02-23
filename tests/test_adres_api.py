import unittest
from postcodepy import postcodepy

import os, sys
#import json

access_key = None
access_secret = None

class TestUM(unittest.TestCase):
    def setUp(self):
      global access_key
      access_key = os.getenv("ACCESS_KEY")
      global access_secret
      access_secret = os.getenv("ACCESS_SECRET")
      if not (access_key and access_secret ):
        print "provide an access key and secret via environment:"
        print "export ACCESS_KEY=..."
        print "export ACCESS_SECRET=..."
        self.skipTest(self)

    def test_PostcodeDataOK(self):
      """ TEST: retrieval of data, should return testvalues for city and street
      """
      api = postcodepy.API( environment='live', access_key=access_key, access_secret=access_secret)
      pc = ('1071XX', 1)
      retValue = api.get_postcodedata( *pc )
      self.assertEqual( (retValue['city'],retValue['street']), ("Amsterdam", "Museumstraat") ) 

    def test_PostcodeDataWithAdditionOK(self):
      """ TEST: retrieval of data, should return testvalues for city, street, housenumber, and housenumber addition
      """
      api = postcodepy.API( environment='live', access_key=access_key, access_secret=access_secret)
      pc = ('7514BP', 129, 'A')
      retValue = api.get_postcodedata( *pc )
      self.assertEqual( (retValue['city'], retValue['street'], retValue['houseNumber'], retValue['houseNumberAddition'] ), ("Enschede", "Lasondersingel", 129, "A") )

    def test_PostcodeDataWithAdditionFail(self):
      """ TEST: retrieval of data, should fail with ERRHouseNumberAdditionInvalid exception
      """
      api = postcodepy.API( environment='live', access_key=access_key, access_secret=access_secret)
      pc = ('7514BP', 129, 'B')
      with self.assertRaises( postcodepy.PostcodeError)  as cm:
        retValue =api.get_postcodedata( *pc )

      caught_exception = cm.exception
      #print >>sys.stderr, "*********\n", caught_exception.response_data['houseNumberAdditions']
      expected_exception = postcodepy.PostcodeError("ERRHouseNumberAdditionInvalid")
      self.assertEqual( expected_exception.exceptionId, caught_exception.exceptionId)

    def test_PostcodeNoData(self):
      """ TEST: no data for this postcode, a request that should fail with PostcodeNl_Service_PostcodeAddress_AddressNotFoundException
      """
      api = postcodepy.API( environment='live', access_key=access_key, access_secret=access_secret)
      pc = ('1077XX', 1)
      with self.assertRaises( postcodepy.PostcodeError)  as cm:
        api.get_postcodedata( *pc )

      caught_exception = cm.exception
      expected_exception = postcodepy.PostcodeError("PostcodeNl_Service_PostcodeAddress_AddressNotFoundException", { 
                                                                          "exception" : "Combination does not exist.",
                                                                        "exceptionId" : "PostcodeNl_Service_PostcodeAddress_AddressNotFoundException"})
      self.assertEqual( expected_exception.msg.decode('utf-8'), caught_exception.msg.decode('utf-8'))

    def test_PostcodeWrongFormat(self):
      """ TEST: no data for this postcode, a request that should fail with PostcodeNl_Controller_Address_InvalidPostcodeException
      """
      api = postcodepy.API( environment='live', access_key=access_key, access_secret=access_secret)
      pc = ('1071 X', 1)
      with self.assertRaises( postcodepy.PostcodeError)  as cm:
        api.get_postcodedata( *pc )

      caught_exception = cm.exception
      expected_exception = postcodepy.PostcodeError("PostcodeNl_Controller_Address_InvalidPostcodeException", { 
                                                                          "exception" : "Postcode does not use format `1234AB`.",
                                                                        "exceptionId" : "PostcodeNl_Controller_Address_InvalidPostcodeException"})
      self.assertEqual( expected_exception.msg.decode('utf-8'), caught_exception.msg.decode('utf-8') )

    def test_PostcodeInvalidUserAccount(self):
      """ TEST: invalid useraccount, test should fail with a PostcodeNl_Controller_Plugin_HttpBasicAuthentication_NotAuthorizedException
      """
      # make the key faulty by adding an extra character
      api = postcodepy.API( environment='live', access_key="1"+access_key, access_secret=access_secret)
      pc = ('1077XX', 1)
      with self.assertRaises( postcodepy.PostcodeError)  as cm:
        api.get_postcodedata( *pc )

      caught_exception = cm.exception

      expected_exception = postcodepy.PostcodeError("PostcodeNl_Controller_Plugin_HttpBasicAuthentication_NotAuthorizedException", { 
                                                                          "exception" : "User `1%s` not correct." % access_key ,
                                                                        "exceptionId" : "PostcodeNl_Controller_Plugin_HttpBasicAuthentication_NotAuthorizedException" })
      self.assertEqual( expected_exception.msg.decode('utf-8'),
                         caught_exception.msg.decode('utf-8'))

    def test_PostcodeInvalidUserSecret(self):
      """ TEST: invalid secret, test should fail with a PostcodeNl_Controller_Plugin_HttpBasicAuthentication_PasswordNotCorrectException
      """
      # make the secret faulty by adding an extra character
      api = postcodepy.API( environment='live', access_key=access_key, access_secret="1"+access_secret)
      pc = ('1077XX', 1)
      with self.assertRaises( postcodepy.PostcodeError)  as cm:
        api.get_postcodedata( *pc )

      caught_exception = cm.exception

      expected_exception = postcodepy.PostcodeError("PostcodeNl_Controller_Plugin_HttpBasicAuthentication_PasswordNotCorrectException", { 
                                                                          "exception" : "Password not correct.",
                                                                        "exceptionId" : "PostcodeNl_Controller_Plugin_HttpBasicAuthentication_PasswordNotCorrectException" })
      self.assertEqual( expected_exception.msg.decode('utf-8'),
                         caught_exception.msg.decode('utf-8'))

    def test_FailArgNotPassedSecret(self):
      """ TEST: no secret provided : a request that should fail with a ERRauthAccessUnknownSecret
      """
      with self.assertRaises( postcodepy.PostcodeError) as cm:
        api = postcodepy.API( environment='live', access_key=access_key)

      caught_exception = cm.exception
      expected_exception = postcodepy.PostcodeError("ERRauthAccessUnknownSecret")
      self.assertEqual( expected_exception.exceptionId, caught_exception.exceptionId)


    def test_FailArgNotPassedKey(self):
      """ TEST: no key provided : a request that should fail with a ERRauthAccessUnknownKey
      """
      with self.assertRaises( postcodepy.PostcodeError) as cm:
        api = postcodepy.API( environment='live', access_secret=access_secret)

      caught_exception = cm.exception
      expected_exception = postcodepy.PostcodeError("ERRauthAccessUnknownKey")
      self.assertEqual( expected_exception.exceptionId, caught_exception.exceptionId)


    def test_request(self):
      """ TEST: faulty URL, a request that should fail with 'A Connection error occurred.'
      """
      api = postcodepy.API( environment='live', access_key=access_key, access_secret=access_secret)
      # Make the REST-API url point to some faulty url
      api.api_url = "https://some/ur/l"
      pc = ('1071 XX', 1)
      with self.assertRaises( postcodepy.PostcodeError)  as cm:
        api.get_postcodedata( *pc )

      caught_exception = cm.exception
      expected_exception = postcodepy.PostcodeError("ERRrequest", { 
                                                         "exception" : "A Connection error occurred.",
                                                       "exceptionId" : "ERRrequest"})
      self.assertEqual( expected_exception.msg.decode('utf-8'), caught_exception.msg.decode('utf-8') )


    def test_signal_customer_transaction_1(self):
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
        #print >>sys.stderr, json.dumps(retValue, indent=4)
        self.assertEqual( { "warningCount" : retValue['warningCount'],
                            "lenOfSignalArray" : len(retValue['signals']),
                          }, { "warningCount" : 1,
                               "lenOfSignalArray" : 6 } )

      except postcodepy.PostcodeError as e:
        print >>sys.stderr, e, e.exceptionId, e.response_data


if __name__ == "__main__":

  unittest.main()

