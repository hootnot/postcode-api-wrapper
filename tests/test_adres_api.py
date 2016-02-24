"""Adres API tests."""
import unittest
import postcodepy
from postcodepy import PostcodeError
from . import unittestsetup

import os
import sys

access_key = None
access_secret = None
api = None


class Test_Adres_API(unittest.TestCase):
    """Tests for Adres API."""

    def setUp(self):
        """setup for tests.

        provides an api instance
        """
        global access_key
        global access_secret
        global api

        try:
            access_key, access_secret = unittestsetup.auth()
        except Exception as e:
            sys.stderr.write("%s" % e)
            exit(2)

        api = postcodepy.API(environment='live',
                             access_key=access_key,
                             access_secret=access_secret)

    def test_PostcodeDataOK(self):
        """TEST: retrieval of data.

        should return testvalues for city and street
        """
        pc = ('1071XX', 1)
        retValue = api.get_postcodedata(*pc)
        self.assertEqual((retValue['city'], retValue['street']),
                         ("Amsterdam", "Museumstraat"))

    def test_PostcodeDataWithAdditionOK(self):
        """TEST: retrieval of data.

        should return testvalues for city, street, housenumber, and
        housenumber addition
        """
        pc = ('7514BP', 129, 'A')
        retValue = api.get_postcodedata(*pc)
        self.assertEqual((retValue['city'],
                          retValue['street'],
                          retValue['houseNumber'],
                          retValue['houseNumberAddition']),
                         ("Enschede", "Lasondersingel", 129, "A"))

    def test_PostcodeDataWithAdditionFail(self):
        """TEST: retrieval of data.

        should fail with ERRHouseNumberAdditionInvalid exception
        """
        pc = ('7514BP', 129, 'B')
        with self.assertRaises(PostcodeError) as cm:
            retValue = api.get_postcodedata(*pc)

        caught_exception = cm.exception
        exp_exception = PostcodeError("ERRHouseNumberAdditionInvalid")
        self.assertEqual(exp_exception.exceptionId,
                         caught_exception.exceptionId)

    def test_PostcodeNoData(self):
        """TEST: no data for this postcode.

        a request that should fail with:
        PostcodeNl_Service_PostcodeAddress_AddressNotFoundException
        """
        pc = ('1077XX', 1)
        with self.assertRaises(PostcodeError) as cm:
            api.get_postcodedata(*pc)

        caught_exception = cm.exception
        expected_exception = PostcodeError(
            "PostcodeNl_Service_PostcodeAddress_AddressNotFoundException", {
                "exception": "Combination does not exist.",
                "exceptionId": "PostcodeNl_Service_PostcodeAddress_"
                               "AddressNotFoundException"})
        self.assertEqual(expected_exception.msg,
                         caught_exception.msg)

    def test_PostcodeWrongFormat(self):
        """TEST: no data for this postcode.

        a request that should fail with:
        PostcodeNl_Controller_Address_InvalidPostcodeException
        """
        pc = ('1071 X', 1)
        with self.assertRaises(PostcodeError) as cm:
            api.get_postcodedata(*pc)

        caught_exception = cm.exception
        expected_exception = PostcodeError(
            "PostcodeNl_Controller_Address_InvalidPostcodeException", {
                "exception": "Postcode does not use format `1234AB`.",
                "exceptionId": "PostcodeNl_Controller_Address_"
                               "InvalidPostcodeException"})
        self.assertEqual(expected_exception.msg,
                         caught_exception.msg)

    def test_PostcodeInvalidUserAccount(self):
        """TEST: invalid useraccount.

        test should fail with:
        PostcodeNl_Controller_Plugin_HttpBasicAuthentication_NotAuthorizedException
        """
        # make the key faulty by adding an extra character
        api = postcodepy.API(environment='live',
                             access_key="1"+access_key,
                             access_secret=access_secret)
        pc = ('1077XX', 1)
        with self.assertRaises(PostcodeError) as cm:
            api.get_postcodedata(*pc)

        caught_exception = cm.exception

        expected_exception = PostcodeError(
            "PostcodeNl_Controller_Plugin_HttpBasicAuthentication_NotAuthorizedException", {
                "exception": "User `1%s` not correct." % access_key,
                "exceptionId": "PostcodeNl_Controller_Plugin_HttpBasicAuthentication_NotAuthorizedException"})
        self.assertEqual(expected_exception.msg,
                         caught_exception.msg)

    def test_PostcodeInvalidUserSecret(self):
        """TEST: invalid secret.

        test should fail with:
        PostcodeNl_Controller_Plugin_HttpBasicAuthentication_PasswordNotCorrectException
        """
        # make the secret faulty by adding an extra character
        api = postcodepy.API(environment='live',
                             access_key=access_key,
                             access_secret="1"+access_secret)
        pc = ('1077XX', 1)
        with self.assertRaises(PostcodeError) as cm:
            api.get_postcodedata(*pc)

        caught_exception = cm.exception

        expected_exception = PostcodeError(
            "PostcodeNl_Controller_Plugin_HttpBasicAuthentication_PasswordNotCorrectException", {
                "exception": "Password not correct.",
                "exceptionId": "PostcodeNl_Controller_Plugin_HttpBasicAuthentication_PasswordNotCorrectException"})
        self.assertEqual(expected_exception.msg,
                         caught_exception.msg)

    def test_FailArgNotPassedSecret(self):
        """TEST: no secret provided.

        a request that should fail with a ERRauthAccessUnknownSecret
        """
        with self.assertRaises(PostcodeError) as cm:
            api = postcodepy.API(environment='live', access_key=access_key)

        caught_exception = cm.exception
        exp_exception = PostcodeError("ERRauthAccessUnknownSecret")
        self.assertEqual(exp_exception.exceptionId,
                         caught_exception.exceptionId)

    def test_FailArgNotPassedKey(self):
        """TEST: no key provided.

        a request that should fail with a ERRauthAccessUnknownKey
        """
        with self.assertRaises(PostcodeError) as cm:
            api = postcodepy.API(environment='live',
                                 access_secret=access_secret)

        caught_exception = cm.exception
        expect_exception = PostcodeError("ERRauthAccessUnknownKey")
        self.assertEqual(expect_exception.exceptionId,
                         caught_exception.exceptionId)

    def test_request(self):
        """TEST: faulty URL.

        a request that should fail with 'A Connection error occurred.'
        """
        # Make the REST-API url point to some faulty url
        api.api_url = "https://some/ur/l"
        pc = ('1071 XX', 1)
        with self.assertRaises(PostcodeError) as cm:
            api.get_postcodedata(*pc)

        caught_exception = cm.exception
        expected_exception = PostcodeError(
                              "ERRrequest", {
                                  "exception": "A Connection error occurred.",
                                  "exceptionId": "ERRrequest"})
        self.assertEqual(expected_exception.msg,
                         caught_exception.msg)


if __name__ == "__main__":

    unittest.main()
