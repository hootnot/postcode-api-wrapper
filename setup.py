import os
import re
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

requirements = map(str.strip, open("requirements.txt").readlines())

version = get_version('postcodepy')

setup(
    name="postcodepy",
    version=version,
    author="Feite Brekeveld",
    author_email="f.brekeveld@gmail.com",
    description=("API-wrapper for postcode.nl REST-API to retrieve relevant "
                 "address information based on 'postal code', or in Dutch: "
                 "postcode/huisnummer"),
    license="MIT",
    keywords="postcode.nl REST API wrapper python",
    url="https://github.com/hootnot/postcode-api-wrapper",
    packages=['postcodepy', 'tests'],
    install_requires=requirements,
    # package_data = { }
    # include_package_data = True,
    # long_description=read('README'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        "Topic :: Utilities",
    ],
    test_suite="tests",
)
