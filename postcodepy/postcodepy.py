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

  def get_postcodedata(self, postcode, nr, **params):
    """
        Get 'postcode' 
    """
    endpoint = 'rest/addresses/%s/%s' % ( postcode, nr)
    return self.request(endpoint, params=params)


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
      raise PostcodeError("ERR_AuthAccessKeyUnknown")
    if not access_secret:
      raise PostcodeError("ERR_AuthAccessSecretKeyUnknown")

    if headers:
      self.client.headers.update(headers)

    # Enable basic authentication
    self.client.auth = ( access_key, access_secret )
    
  def request(self, endpoint, method='GET', params=None):
        """Returns dict of response from OANDA's open API
        """
        url = '%s/%s' % ( self.api_url, endpoint)

        method = method.lower()
        params = params or {}

        func = getattr(self.client, method)
        request_args = {}
        if method == 'get':
            request_args['params'] = params
        else:
            request_args['data'] = params

        try:
            response = func(url, **request_args)
        except requests.RequestException as e:
            print (str(e))
        content = response.content.decode('utf-8')

        content = json.loads(content)

        # error message
        if response.status_code >= 400:
            raise PostcodeError("ERRnoData")

        return content

class PostcodeError(Exception):
    """
        Generic error class, catches response errors
    """
    __msgs = { "ERRnoPractice" : "For now there is no practice environment: 'live' is the only valid option",
               "ERRnoData" : "No data found",
               "ERR_AuthAccessKeyUnknown" : "Auth accesskey unknown",
               "ERR_AuthAccessSecretKeyUnknown" : "Auth secret unknown",
             }
    def __init__(self, error_response):
        msg = "Postcode API returned error code %s: '%s'" % \
           ( error_response, self.__msgs[error_response] )

        super(PostcodeError, self).__init__(msg)


# ----------------------------------------------------------------------
if __name__ == "__main__":
  import sys
  """First and third are OK, the 2nd is not OK and raises an Exception
     the exception is written to stderr
  """
  api = API( environment='live', access_key="", access_secret="")
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
    
