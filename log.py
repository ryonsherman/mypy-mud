#!/usr/bin/env python2

__author__    = "Ryon Sherman"
__email__     = "ryon.sherman@gmail.com"
__copyright__ = "Copyright 2014, Ryon Sherman"
__license__   = "MIT"

import logging

# initialize logger
logger = logging.getLogger()
# set default log level
logger.setLevel(logging.DEBUG)
# define log format
logger.format = "[%(asctime)s] (%(levelname)s) %(message)s"
