Installation
============

Introduction
------------

The postcode-api-wrapper package offers a simple API to the Postcode.nl API REST service.
To use the API-service you will need an *access_key* and *access_secret*. For details check api.postcode.nl_.

.. _api.postcode.nl: https://api.postcode.nl


Download & Install
------------------

From pypi
```````````

Install the package with pip::

    $ pip install postcodepy

You may consider using *virtualenv* to create isolated Python environments. Python 3.4 has *pyvenv* providing
the same kind of functionality.


From Github
```````````

.. code-block:: shell

    $ git clone https://github.com/hootnot/postcode-api-wrapper.git
    $ cd postcode-api-wrapper

    Run the tests:
    $ python setup.py test
    $ python setup.py install

