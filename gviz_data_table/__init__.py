"""
Google Visualisation for Python

Convert Python data structures to JSON suitable for the Google Visualisation
Library
"""
import sys
import json

# hack float formatting in Python 2.6
if sys.version_info < (2, 7):
    json.encoder.FLOAT_REPR = lambda o: format(o, '.15g')

#convenience imports
from .table import Table
from .encoder import encode
