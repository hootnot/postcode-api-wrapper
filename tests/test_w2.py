import unittest
from postcodepy import postcodepy

import os, sys

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
      retValue = api.get_postcodedata( pc[0], pc[1] )
      self.assertEqual( retValue['city'], "Amsterdam" ) and \
            self.assertEqual( retValue['street'], "Museumstraat" ) 

    def test_PostcodeNoData(self):
      """ TEST: no data for this postcode, a request that should fail with APIServerERRuserInputError
      """
      api = postcodepy.API( environment='live', access_key=access_key, access_secret=access_secret)
      pc = ('1077XX', 1)
      with self.assertRaises( postcodepy.PostcodeError)  as cm:
        api.get_postcodedata( pc[0], pc[1] )

      caught_exception = cm.exception
      expected_exception = postcodepy.PostcodeError("APIServerERRuserInputError", { "exception" : "Combination does not exist.",
                                                                        "exceptionId" : "PostcodeNl_Service_PostcodeAddress_AddressNotFoundException"})
      self.assertEqual( expected_exception.msg.decode('utf-8'),
                         caught_exception.msg.decode('utf-8'))

    def test_PostcodeInvalidUserAccount(self):
      """ TEST: invalid useraccount, test should fail with APIServerERRuserInputError
      """
      api = postcodepy.API( environment='live', access_key="1"+access_key, access_secret=access_secret)
      pc = ('1077XX', 1)
      with self.assertRaises( postcodepy.PostcodeError)  as cm:
        api.get_postcodedata( pc[0], pc[1] )

      caught_exception = cm.exception

      expected_exception = postcodepy.PostcodeError("APIServerERRuserInputError", { "exception" : "User `1%s` not correct." % access_key ,
                                                                        "exceptionId" : "PostcodeNl_Controller_Plugin_HttpBasicAuthentication_NotAuthorizedException" })
      self.assertEqual( expected_exception.msg.decode('utf-8'),
                         caught_exception.msg.decode('utf-8'))

    def test_PostcodeInvalidUserSecret(self):
      """ TEST: invalid secret, test should fail with APIServerERRuserInputError
      """
      api = postcodepy.API( environment='live', access_key=access_key, access_secret="1"+access_secret)
      pc = ('1077XX', 1)
      with self.assertRaises( postcodepy.PostcodeError)  as cm:
        api.get_postcodedata( pc[0], pc[1] )

      caught_exception = cm.exception

      expected_exception = postcodepy.PostcodeError("APIServerERRuserInputError", { "exception" : "Password not correct.",
                                                                        "exceptionId" : "PostcodeNl_Controller_Plugin_HttpBasicAuthentication_PasswordNotCorrectException" })
      self.assertEqual( expected_exception.msg.decode('utf-8'),
                         caught_exception.msg.decode('utf-8'))

    def test_FailArgNotPassedSecret(self):
      """ TEST: no secret provided : a request that should fail 
      """
      with self.assertRaises( postcodepy.PostcodeError) as cm:
        api = postcodepy.API( environment='live', access_key=access_key)

      caught_exception = cm.exception
      expected_exception = postcodepy.PostcodeError("ERRauthAccessUnknownSecret")
      self.assertEqual( expected_exception.error_code, caught_exception.error_code)


    def test_FailArgNotPassedKey(self):
      """ TEST: no key provided : a request that should fail 
      """
      with self.assertRaises( postcodepy.PostcodeError) as cm:
        api = postcodepy.API( environment='live', access_secret=access_secret)

      caught_exception = cm.exception
      expected_exception = postcodepy.PostcodeError("ERRauthAccessUnknownKey")
      self.assertEqual( expected_exception.error_code, caught_exception.error_code)

if __name__ == "__main__":

  unittest.main()

