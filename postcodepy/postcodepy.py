import json
import requests

""" Postcode API wrapper for Postcode.nl REST API

    This code is inspired on the oandapy.py wrapper for the OANDA-API 
"""

""" The simple version:
    ----------------------
    from requests.auth import HTTPBasicAuth
    key, secret = ... , ...
    auth=HTTPBasicAuth(key, secret)
    response = requests.get("https://api.postcode.nl/rest/addresses/1077XX/1", auth=auth)
    print response
    print response.content
"""

""" EndpointsMixin provides a mixin for the API instance
    Parameters that need to be embedded in the API url just need to be passes as a keyword argument.
"""

class EndpointsMixin(object):

  def get_postcodedata(self, postcode, nr, addition="", **params):
    """
        Get 'postcode' 
    """
    endpoint = 'rest/addresses/%s/%s' % ( postcode, nr)
    if addition:
      endpoint += '/' + addition

    retValue = self.request(endpoint, params=params)

    # then it should match the houseNumberAdditions
    if addition and not ( retValue.has_key('houseNumberAddition') and addition == retValue['houseNumberAddition']):
      raise PostcodeError("ERRHouseNumberAdditionInvalid", { "exceptionId" : "ERRHouseNumberAdditionInvalid",
                                                               "exception" : "Invalid housenumber addition: '%s'" % retValue['houseNumberAddition'],
                                               "validHouseNumberAdditions" : retValue['houseNumberAdditions'] } )

    return retValue

  def get_signalcheck(self, sar, **params):
    """
        Get 'signal check'
    """
    params = sar
    endpoint = 'rest/signal/check'

    # The 'sar'-request dictionary should be sent as valid JSON data, so we need to convert it to JSON
    # when we construct the request in API.request
    retValue = self.request(endpoint, 'POST', params=params, convJSON=True)

    return retValue


class API(EndpointsMixin, object):

  def __init__(self, environment="practice", access_key=None, access_secret=None, headers=None ):
    """ Instantiate API wrapper
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
    self.client.auth = ( access_key, access_secret )
    
  def request(self, endpoint, method='GET', params=None, convJSON=False):
        """Returns dict of response from postcode.nl API
        """
        url = '%s/%s' % ( self.api_url, endpoint)

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
            """ Normally some valid HTTP-response will be the case
                if not some exception regarding the request / connection has occurred
                this will be one of the exceptions of the request module
                if so, we will a PostcodeError exception and pass the request exception message
            """
            response = func(url, **request_args)
        except requests.RequestException as e:
            raise PostcodeError("ERRrequest", { "exception" : e.__doc__ } )

        content = response.content.decode('utf-8')

        content = json.loads(content)

        if response.status_code == 200:
          return content

        # Errors, otherwise we did not get here ...
        if content.has_key('exceptionId'):
            raise PostcodeError(content['exceptionId'], content)
        
        raise PostcodeError("UnknownExceptionFromPostcodeNl")


class PostcodeError(Exception):
    """
        Generic error class, catches response errors
    """

    exceptionId  = None
    response_data  = None
    msg = None
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
              'React_Model_Property_Validation_Number_ValueTooHighException',
              'PostcodeNl_Service_PostcodeAddress_AddressNotFoundException',
              #
              'ERRHouseNumberAdditionInvalid',
              # NEEDS TO BE LAST !
              'ERRUnknownExceptionFromPostcodeNl',
    ]

    def __init__(self, exceptionId, response_data=None):
        self.exceptionId = exceptionId if exceptionId in self.__eid else self.__eid[-1]
        self.response_data = response_data

        self.msg = ""

        # add additional data if we have it
        if response_data and response_data.has_key('exception'):
          self.msg += response_data['exception']

        super(PostcodeError, self).__init__(self.msg)


# ----------------------------------------------------------------------
if __name__ == "__main__":
  import sys, os
  """First and third are OK, the 2nd is not OK and raises an Exception
     the exception is written to stderr
  """
  api = API( environment='live', access_key=os.getenv("ACCESS_KEY"), access_secret=os.getenv("ACCESS_SECRET"))
  for pc in [ ('1071XX', 1), ('8422DH', 34, 'B'), ('1077XX', 1), ('7514BP', 129) ]:
    try:
      retValue = api.get_postcodedata( *pc )
      # the raw resultvalue
      print retValue
      # The parsed result 
      print "\nresults for: ", pc
      for K in retValue.keys():
        try:
          print "%30s : %s" % (K, retValue[K] )
        except Exception, e:
          print "ERROR: ", K, retValue[K]

    except PostcodeError, e:
      print >>sys.stderr, e, pc, e.exceptionId, e.response_data
    
