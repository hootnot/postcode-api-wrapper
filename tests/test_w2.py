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

    def test_Postcode(self):
      """ test retrieval of data
      """
      api = postcodepy.API( environment='live', access_key=access_key, access_secret=access_secret)
      pc = ('1071XX', 1)
      retValue = api.get_postcodedata( pc[0], pc[1] )
      self.assertEqual( retValue['city'], "Amsterdam" ) and \
            self.assertEqual( retValue['street'], "Museumstraat" ) 

    def test_PostcodeFail(self):
      """ no data for this postcode, a request that should fail 
      """
      api = postcodepy.API( environment='live', access_key=access_key, access_secret=access_secret)
      pc = ('1077XX', 1)
      self.assertRaises( postcodepy.PostcodeError, lambda: api.get_postcodedata( pc[0], pc[1] ))

    def test_SecretFail(self):
      """ no secret : a request that should fail 
      """
      self.assertRaises( postcodepy.PostcodeError,  lambda: postcodepy.API( environment='live', access_key=access_key))

    def test_KeyFail(self):
      """ no key : a request that should fail 
      """
      self.assertRaises( postcodepy.PostcodeError,  lambda: postcodepy.API( environment='live', access_secret=access_secret))

if __name__ == "__main__":

  unittest.main()

