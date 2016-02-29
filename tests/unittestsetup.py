"""Provide generic authentication for tests."""
import os


def auth():
    """auth - reads access_key and access_secret from file.

    Tests should use this method to provide authentication for the API
    """
    access_key = os.getenv("ACCESS_KEY")
    access_secret = os.getenv("ACCESS_SECRET")

    if "" in [access_key, access_secret]:
        raise Exception("\n"
                        "*******************************************************\n"
                        "*** TO RUN THE TESTS:                               ***\n"
                        "*** please provide env ACCESS_KEY and ACCESS_SECRET ***\n"
                        "*******************************************************\n")

    return access_key, access_secret
