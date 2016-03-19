"""Postcode API module."""
import json
import requests


class EndpointsMixin(object):
    """EndpointsMixin - API endpoints for the API class.

    each endpoint of the API has a representative method in EndpointsMixin
    Parameters that apply to the API url just need to be passed
    as a keyword argument.
    """

    def get_postcodedata(self, postcode, nr, addition="", **params):
        """get_postcodedata - fetch information for 'postcode'.

        Parameters
        ----------
        postcode : string
            The full (dutch) postcode

        nr : int
            The housenumber

        addition : string (optional)
            the extension to a housenumber

        params : dict (optional)
            a list of parameters to send with the request.

        returns :
            a response dictionary
        """
        endpoint = 'rest/addresses/%s/%s' % (postcode, nr)
        if addition:
            endpoint += '/' + addition

        retValue = self._API__request(endpoint, params=params)

        # then it should match the houseNumberAdditions
        if addition and addition.upper() not in \
           [a.upper() for a in retValue['houseNumberAdditions']]:
            raise PostcodeError(
                    "ERRHouseNumberAdditionInvalid",
                    {"exceptionId": "ERRHouseNumberAdditionInvalid",
                     "exception": "Invalid housenumber addition: '%s'" %
                     retValue['houseNumberAddition'],
                     "validHouseNumberAdditions":
                     retValue['houseNumberAdditions']})

        return retValue

    def get_signalcheck(self, sar, **params):
        """get_signalcheck -  perform a signal check.

        Parameters
        ----------
        sar : dict
            signal-api-request specified as a dictionary of parameters.
            All of these parameters are optional. For details
            check https://api.postcode.nl/documentation/signal-api-example.

        returns :
            a response dictionary
        """
        params = sar
        endpoint = 'rest/signal/check'

        # The 'sar'-request dictionary should be sent as valid JSON data, so
        # we need to convert it to JSON
        # when we construct the request in API.request
        retValue = self._API__request(endpoint, 'POST',
                                      params=params, convJSON=True)

        return retValue


class API(EndpointsMixin, object):
    """API - postcode API class."""

    def __init__(self, environment="practice", access_key=None,
                 access_secret=None, headers=None):
        """Instantiate API wrapper.

        Parameters
        ----------
        environment : str
           the environment to use. Currently only 'live'.

        access_key : str
            the access key provided by postcode.nl . If not provided
            an ERRauthAccessUnknownKey exception is raised

        access_secret : str
            the access secret provided by postcode.nl . If not provided
            an ERRauthAccessUnknownSecret exception is raised

        headers : dict
            optional headers to set

        returns :
            a response dictionary
        """
        if environment == 'practice':
            raise PostcodeError("ERRnoPractice")
        elif environment == 'live':
            self.api_url = 'https://api.postcode.nl'

        self.client = requests.Session()

        if not access_key:
            raise PostcodeError("ERRauthAccessUnknownKey")
        if not access_secret:
            raise PostcodeError("ERRauthAccessUnknownSecret")

        if headers:
            self.client.headers.update(headers)

        # Enable basic authentication
        self.client.auth = (access_key, access_secret)

    def __request(self, endpoint, method='GET', params=None, convJSON=False):
        """request - Returns dict of response from postcode.nl API.

        This method is called only by the EndpointMixin methods.
        """
        url = '%s/%s' % (self.api_url, endpoint)

        method = method.lower()
        params = params or {}
        if convJSON:
            params = json.dumps(params)

        func = getattr(self.client, method)
        request_args = {}
        if method == 'get':
            request_args['params'] = params
        else:
            request_args['data'] = params

        try:
            # Normally some valid HTTP-response will be the case
            # if not some exception regarding the request / connection has
            # occurred
            # this will be one of the exceptions of the request module
            # if so, we will a PostcodeError exception and pass the request
            # exception message
            response = func(url, **request_args)
        except requests.RequestException as e:
            raise PostcodeError("ERRrequest", {"exception": e.__doc__})

        content = response.content.decode('utf-8')

        content = json.loads(content)

        if response.status_code == 200:
            return content

        # Errors, otherwise we did not get here ...
        if 'exceptionId' in content:
            raise PostcodeError(content['exceptionId'], content)

        raise PostcodeError("UnknownExceptionFromPostcodeNl")


class PostcodeError(Exception):
    """PostcodeError - Generic error class, catches response errors."""

    __eid = [
            # Request exceptions
            'ERRrequest',
            # Module exceptions
            'ERRnoPractice',
            'ERRauthAccessUnknownKey',
            'ERRauthAccessUnknownSecret',
            # API exceptions
            'PostcodeNl_Controller_Plugin_HttpBasicAuthentication_Exception',
            'PostcodeNl_Controller_Plugin_HttpBasicAuthentication_NotAuthorizedException',
            'PostcodeNl_Api_RestClient_AuthenticationException',
            'PostcodeNl_Controller_Plugin_HttpBasicAuthentication_PasswordNotCorrectException',
            'React_Controller_Action_InvalidParameterException',
            'PostcodeNl_Controller_Address_InvalidPostcodeException',
            'PostcodeNl_Controller_Address_InvalidHouseNumberException',
            'PostcodeNl_Controller_Address_NoPostcodeSpecifiedException',
            'PostcodeNl_Controller_Address_NoHouseNumberSpecifiedException',
            'PostcodeNl_Controller_Address_PostcodeTooLongException',
            'React_Model_Property_Validation_Number_ValueTooHighException',
            'PostcodeNl_Service_PostcodeAddress_AddressNotFoundException',
            #
            'ERRHouseNumberAdditionInvalid',
            # NEEDS TO BE LAST !
            'ERRUnknownExceptionFromPostcodeNl',
    ]

    def __init__(self, exceptionId, response_data=None):
        """instantiate PostcodeError instance.

        Parameters
        ----------
        exceptionId : str
            the id of the exception. It should match one of the known exception
            id's. If it does not match it is set to:
            ERRUnknownExceptionFromPostcodeNl

        response_data : data
            the data received at the moment the exception occurred
        """
        if exceptionId in self.__eid:
            self.exceptionId = exceptionId
        else:
            self.exceptionId = self.__eid[-1]
        self.response_data = response_data

        self.msg = ""

        # add additional data if we have it
        if response_data and "exception" in response_data:
            self.msg += response_data['exception']

        super(PostcodeError, self).__init__(self.msg)


# ----------------------------------------------------------------------
if __name__ == "__main__":    # pragma: no cover
    import sys
    import os
    # First and third are OK, the 2nd is not OK and raises an Exception
    # the exception is written to stderr

    api = API(environment='live', access_key=os.getenv("ACCESS_KEY"),
              access_secret=os.getenv("ACCESS_SECRET"))
    for pc in [('1071XX', 1),
               ('1077XX', 1),
               ('7514BP', 129),
               ('7514BP', 129, 'A'),
               ('7514BP', 129, 'a'),
               ('7514BP', 129, 'b'),
               ]:
        try:
            retValue = api.get_postcodedata(*pc)
            print("\nresults for: {}".format(str(pc)))
            print(json.dumps(retValue, sort_keys=True, indent=2))

        except PostcodeError as e:
            sys.stderr.write("{}, {}, {}".format(
                             str(pc), e.exceptionId,
                             json.dumps(e.response_data,
                                        sort_keys=True,
                                        indent=2)))
