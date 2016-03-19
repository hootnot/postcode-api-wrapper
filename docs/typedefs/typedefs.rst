Typedefs
----------

.. automodule:: postcodepy.typedefs
      :members:

.. exec::
   import json
   from postcodepy.typedefs import POSTCODE_API_TYPEDEFS_ADDRESS_TYPES
   lines = [ "    POSTCODE_API_TYPEDEFS_ADDRES_TYPES = " ]
   for x in json.dumps(POSTCODE_API_TYPEDEFS_ADDRESS_TYPES,
                       indent=4).split("\n"):
       lines.append("    {}".format(x))
   print("\n\n.. code-block:: python\n\n{}\n\n".format("\n".join(lines)))

.. exec::
   import json
   from postcodepy.typedefs import POSTCODE_API_TYPEDEFS_PURPOSES 
   lines = [ "    POSTCODE_API_TYPEDEFS_PURPOSES = " ]
   for x in json.dumps(POSTCODE_API_TYPEDEFS_PURPOSES, indent=4).split("\n"):
       lines.append("    {}".format(x))
   print("\n\n.. code-block:: python\n\n{}\n\n".format("\n".join(lines)))

The REST responses may contain fields that can be translated into the standard
descriptions as provided by postcode.nl.
This translation can be accomplished by simply applying the decorators to a
function that parses the return value of the API-call.


Logging
~~~~~~~

In case values can't be translated, a warning is logged by `logger`. The
message will contain the `postcode` that was responsible for the warning.
