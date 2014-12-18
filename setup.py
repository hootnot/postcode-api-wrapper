import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requirements = map(str.strip, open("requirements.txt").readlines())

setup(
    name = "postcodepy",
    version = "0.0.4",
    author = "Feite Brekeveld",
    author_email = "f.brekeveld@gmail.com",
    description = ("API-wrapper for postcode.nl REST-API to retrieve relevant address information based on 'postal code', or in Dutch: postcode/huisnummer"),
    license = "MIT",
    keywords = "postcode.nl REST API wrapper python",
    url = "https://github.com/hootnot/postcode-api-wrapper",
    packages=['postcodepy', 'tests'],
    install_requires = requirements,
    #package_data = { }
    #include_package_data = True,
    long_description=read('README'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
    ],
    test_suite="tests",
)

