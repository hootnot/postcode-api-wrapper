Examples
--------

Get information by ``postcode``:

.. code-block:: python

    import sys
    import os
    # First and third are OK, the 2nd is not OK and raises an Exception
    # the exception is written to stderr

    api = API(environment='live',
              access_key=os.getenv("ACCESS_KEY"),
              access_secret=os.getenv("ACCESS_SECRET"))
    for pc in [('1071XX', 1),
               ('8422DH', 34, 'B'),
               ('1077XX', 1),
               ('7514BP', 129)]:
        try:
            retValue = api.get_postcodedata(*pc)
            # the raw resultvalue
            print(retValue)
            # The parsed result
            print("\nresults for: ", pc)
            for K in retValue.keys():
                try:
                    print("%30s : %s" % (K, retValue[K]))
                except Exception, e:
                    print("ERROR: ", K, retValue[K])

        except PostcodeError as e:
            sys.stderr.write("%s, %s, %s, %s" %
                             (e, pc, e.exceptionId, e.response_data))
