#!/usr/bin/env python2

__author__    = "Ryon Sherman"
__email__     = "ryon.sherman@gmail.com"
__copyright__ = "Copyright 2015, Ryon Sherman"
__license__   = "MIT"

import logging

# define log format
LOG_FORMAT = "[%(asctime)s] (%(levelname)s) %(message)s"
# define log time format
LOG_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# get root logger
log = logging.getLogger()
# set default logging level
log.setLevel(logging.DEBUG)
# set log formats
log.LOG_FORMAT = LOG_FORMAT
log.LOG_TIME_FORMAT = LOG_TIME_FORMAT

# intitialize log formatter
formatter = logging.Formatter(LOG_FORMAT)

# wrapper to return message after logging
def log_return(fn):
    def wrapper(msg, *args, **kwargs):
        if not log.handlers: return
        fn(msg, *args, **kwargs)
        return msg
    return wrapper
map(lambda fn: setattr(log, fn, log_return(getattr(log, fn))), (
    'info', 'warning', 'error', 'critical', 'exception'))

# log handler helper
def setLogHandler(handler, lvl=logging.DEBUG):
    handler.setFormatter(formatter)
    handler.setLevel(lvl)
    log.addHandler(handler)
log.setLogHandler = setLogHandler

# console log handler helper
def setConsoleLogHandler(msg, lvl=logging.INFO):
    setLogHandler(logging.StreamHandler(), lvl)
    if msg: log.info(msg)
log.setConsoleLogHandler = setConsoleLogHandler

# file log handler helper
def setFileLogHandler(logfile):
    setLogHandler(logging.FileHandler(logfile))
log.setFileLogHandler = setFileLogHandler