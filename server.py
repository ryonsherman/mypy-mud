#!/usr/bin/env python2

__author__    = "Ryon Sherman"
__email__     = "ryon.sherman@gmail.com"
__copyright__ = "Copyright 2015, Ryon Sherman"
__license__   = "MIT"

import socket
import asyncore

from log import log
from console import Console


class Server(asyncore.dispatcher):
    # default port
    port = 10000
    # default address
    address = '0.0.0.0'

    def __init__(self, address=address, port=port, *args, **kwargs):        
        # initialize dispatcher
        asyncore.dispatcher.__init__(self, *args, **kwargs)

        # initialize server properties
        self.port = int(port)
        self.address = address
        self.connection = (self.address, self.port)        

    def start(self, msg=None):
        # log request
        if not self.connected: 
            log.info(msg or "Starting server...")
        else:
            log.warning(msg or "Server already started!")
            return False

        # attempt to listen on socket
        try: 
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.set_reuse_addr()
            self.bind(self.connection)
            self.listen(5)
        except Exception as e: 
            return self.stop(e)        
        self.connected = True

        # log success
        log.info("Server started.")
        log.info("Awaiting connections at [%s:%s]..." % self.connection)

        # start dispatcher
        asyncore.loop()

    def stop(self, msg=None):
        # log request
        if self.connected: 
            log.info(msg or "Stopping server...")
        else:
            log.warning(msg or "Server not started!")
            return False

        # close socket
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(self.connection)
        self.close()

        # log success
        log.info("Server stopped.")


# define main method
def main():
    import argparse 

    # initialize argument parser
    parser = argparse.ArgumentParser()

    # define 'address' argument
    parser.add_argument('--address', 
        default=Server.address,
        help="Bound interface address (default: %(default)s)")

    # define 'port' argument
    parser.add_argument('--port', 
        type=int, 
        default=Server.port,
        help="Bound port number (default: %(default)s)")

    # parse arguments
    args = parser.parse_args()

    # TODO: --log LVL
    log.setConsoleLogHandler("Console logging enabled")
    # TODO: --file FILE

    # initialize server
    server = Server(args.address, args.port)
    
    # TODO: --console
    # initialize server console
    console = Console(server)
    try:
        while True:
            console.command(raw_input(console.prompt))
    except (KeyboardInterrupt, EOFError):
        console.stop()


# execute main method
if __name__ == '__main__':
    main()
