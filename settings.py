import os

from os.path import abspath, basename, dirname, join, normpath
from sys import path


########## PATH CONFIGURATION
PROJECT_ROOT = dirname(abspath(__file__))

ENDPOINTS_ROOT = "%s/endpoints/" % PROJECT_ROOT

