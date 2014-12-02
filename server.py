#!/usr/bin/env python2

__author__    = "Ryon Sherman"
__email__     = "ryon.sherman@gmail.com"
__copyright__ = "Copyright 2014, Ryon Sherman"
__license__   = "MIT"

import socket
import logging
import asyncore

from log import logger
from client import Client


class Server(asyncore.dispatcher):
    # default port
    port = 10000
    # default address
    address = '0.0.0.0'

    def __init__(self, **kwargs):        
        # initialize dispatcher
        asyncore.dispatcher.__init__(self)
        # create socket
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        # reuse address
        self.set_reuse_addr()
        # assign server properties        
        self.port    = int(kwargs.get('port', self.port))
        self.address = kwargs.get('address', self.address)
        # assign instance properties
        self.clients = []

    def start(self):
        # log server start request
        logger.info("Starting server...")
        # bind to socket
        self.bind((self.address, self.port))
        # listen on socket
        self.listen(5)
        # log server start
        logger.info("Server started. Awaiting connections at [%s:%s]..." %
            (self.address, self.port))
        # start server loop
        asyncore.loop()
        # stop server
        self.stop()

    def stop(self):
        # log server stop request
        logger.info("Stopping server...")        
        # close server socket
        self.close()
        # log server stop
        logger.info("Server stopped.")
        # end server loop
        raise asyncore.ExitNow

    def handle_accept(self):
        # accept connection
        connection = self.accept()
        # return if connection is invalid
        if connection is None:
            return

        # initialize client
        client = Client(self, connection)
        # log connection
        logger.info("Client [%s] connected." % client.address)
        # append client to server clients
        self.clients.append(client)


if __name__ == '__main__':
    import argparse
    # initialize argument parser
    parser = argparse.ArgumentParser()
    # define 'address' argument
    parser.add_argument('--address', default=Server.address,
        help="Bound interface address (default: %(default)s)")
    # define 'port' argument
    parser.add_argument('--port', type=int, default=Server.port,
        help="Server port (default: %(default)s)")
    # define 'log' argument
    parser.add_argument('--log',
        default='./pymud.log',
        help="Log path (default: %(default)s)")
    # define 'log_level' argument
    parser.add_argument('--log_level', default='INFO',
        choices=['ERROR', 'INFO', 'DEBUG'],
        help="Console log level (default: %(default)s)")
    # define 'silent' argument
    parser.add_argument('--silent', default=False,
        action='store_true',
        help="Disable console log output")
    # parse arguments
    args = parser.parse_args()

    # intitialize log formatter
    formatter = logging.Formatter(logger.format)
    # if console output requested
    if not args.silent:        
        # determine log level
        log_level = getattr(logging, args.log_level.upper())
        # set console log handler
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.setLevel(log_level)
        logger.addHandler(handler)
    # set file log handler
    handler = logging.FileHandler(args.log)
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)

    # initialize server
    server = Server(
        port=args.port,
        address=args.address
    )
    try:
        # run server loop
        server.start()
    except (KeyboardInterrupt, SystemExit):
        try:
            # interrupt server loop
            server.stop()
        except asyncore.ExitNow:
            pass
    except asyncore.ExitNow:
            pass
