"""Provide generic authentication for tests."""


def auth():
    """auth - reads access_key and access_secret from file.

    Tests should use this method to provide authentication for the API
    """
    access_key = None
    access_secret = None
    with open("tests/access_key.txt") as I:
        access_key = I.read().strip()
    with open("tests/access_secret.txt") as I:
        access_secret = I.read().strip()

    if "xxxx" in [access_key, access_secret]:
        raise Exception("\n"
                        "*************************************************\n"
                        "*** TO RUN THE TESTS:                         ***\n"
                        "*** PLEASE PROVIDE YOUR access_key AND secret ***\n"
                        "*** IN access_key.txt AND access_secret.txt   ***\n"
                        "*************************************************\n")

    return access_key, access_secret
