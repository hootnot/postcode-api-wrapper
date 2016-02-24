"""signal API tests."""
import unittest
import postcodepy

import os
import sys
from . import unittestsetup

access_key = None
access_secret = None
api = None


class Test_Signal_API(unittest.TestCase):

    def setUp(self):
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

    def test_signal_customer_transaction_1(self):
        """ TEST: signal check URL, a request that should report:
        1 warning with 4 signals
        """

        retValue = None
        try:
            dct = {"customer": {
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

            retValue = api.get_signalcheck(dct)
            # sys.stderr.write("%s" % json.dumps(retValue, indent=4))
            self.assertEqual({"warningCount": retValue['warningCount'],
                              "lenOfSignalArray": len(retValue['signals']),
                              },
                             {"warningCount": 1,
                              "lenOfSignalArray": 4
                              })

        except postcodepy.PostcodeError as e:
            sys.stderr.write("%s, %s, %s\n" %
                             (e, e.exceptionId, e.response_data))


if __name__ == "__main__":

    unittest.main()
