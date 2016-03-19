"""Type definitions."""
import logging
from functools import wraps

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

POSTCODE_API_TYPEDEFS_ADDRESS_TYPES = {
    "building": "verblijfsobject",
    "house boat site": 'location used for mooring house boats',
    "mobile home site": 'location used for mobile homes and trailers',
    "PO box": 'PO box',
}

POSTCODE_API_TYPEDEFS_PURPOSES = {
    "residency": "woonfunctie",
    "assembly": "bijeenkomstfunctie",
    "detention": "celfunctie",
    "healthcare": "gezondheidszorgfunctie",
    "industry": "industriefunctie",
    "office": "kantoorfunctie",
    "lodging": "logiesfunctie",
    "education": "onderwijsfunctie",
    "sport": "sportfunctie",
    "shopping": "winkelfunctie",
    "other": "overige gebruiksfunctie",
}

SIGNAL_API_TYPEDEFS = {
    # signalTransactionStatus
    "new": "The transaction is being constructed, but has not yet been " +
           "agreed upon. (customer is shopping)",
    "new-checkout": "The transaction is being constructed, and customer is a" +
                    " checkout process",
    "pending": "The transaction is agreed upon, but customer needs to "
               "complete some final steps.",
    "pending-payment": "The transaction is agreed upon, but customer needs "
                       "to complete the payment process.",
    "processing": "Customer has finished all steps of transaction creation, "
                  "shop needs to package & ship order.",
    "complete": "The transaction has been shipped. (but not necessarily "
                "delivered)",
    "closed": "The transaction has been shipped, and (assumed) delivered, "
              "cannot be cancelled anymore.",
    "cancelled": "The transaction cancelled from any state. The transaction "
                 "will not continue and will not be restarted later.",
    "cancelled-by-customer": "The transaction was cancelled by the customer.",
    "cancelled-by-shop": "The transaction was cancelled by the shop.",
    "onhold": "The transaction needs some custom interaction by customer or "
              "shop before it can continue.",
    "other": "Another status not listed here.",
}


def translate_addresstype(f):
    """decorator to translate the addressType field.

    translate the value of the addressType field of the API response into a
    translated type.
    """
    @wraps(f)
    def wr(r, pc):
        at = r["addressType"]
        try:
            r.update({"addressType": POSTCODE_API_TYPEDEFS_ADDRESS_TYPES[at]})
        except:
            logger.warning("Warning: {}: "
                           "unknown 'addressType': {}".format(pc, at))

        return f(r, pc)

    return wr


def translate_purposes(f):
    """decorator to translate the purposes field.

    translate the values of the purposes field of the API response into
    translated values.
    """
    @wraps(f)
    def wr(r, pc):
        tmp = []
        for P in r["purposes"]:
            try:
                tmp.append(POSTCODE_API_TYPEDEFS_PURPOSES[P])
            except:
                logger.warning("Warning: {}: "
                               "cannot translate 'purpose': {}".format(pc, P))
                tmp.append(P)

        r.update({"purposes": tmp})
        return f(r, pc)

    return wr
