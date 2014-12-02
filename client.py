#!/usr/bin/env python2

__author__    = "Ryon Sherman"
__email__     = "ryon.sherman@gmail.com"
__copyright__ = "Copyright 2014, Ryon Sherman"
__license__   = "MIT"

import socket
import logging
import asyncore
import importlib

from log import logger
from players import Player

# define data chunk size and terminator
CHUNK_SIZE = 8192
TERMINATOR = '\r\n'


class Dispatcher(asyncore.dispatcher_with_send):
    def __init__(self, (sock, addr)):
        # initialize dispatcher
        asyncore.dispatcher_with_send.__init__(self, sock)
        # assign socket properties        
        self.buffer   = ''
        self.callback = None
        self.address  = ':'.join(map(str, addr))

    def prompt(self, msg, callback=None):
        self.write(msg, False)
        self.callback = callback

    def write(self, data, terminate=True):
        # append terminator if not terminated
        if terminate and not data.endswith(TERMINATOR):
            data += TERMINATOR
        # send message
        self.send(data)

        # log write
        logger.debug("Client write(%d) > [%s]: %s" % (
            len(data), self.address, data.strip()))

    def read(self):
        # return if buffer has no data
        if not self.buffer: return

        # get buffered data
        data = self.buffer.strip()
        # reset data buffer
        self.buffer = ''
        # get data callback
        callback = self.callback
        # reset data callback
        self.callback = None

        # perform callback if requested
        if callback: return callback(data)

        # return data
        return data

    def handle_read(self):
        # receive a chunk of data
        data = self.recv(CHUNK_SIZE)
        # return if no data received
        if not data: return

        # log read
        logger.debug("Client read(%d) < [%s]: %s" % (
            len(data), self.address, data.strip()))

        # append data to buffer
        self.buffer += data
        # read buffer if data is terminated
        if data.endswith(TERMINATOR):
            return self.read()

    def handle_close(self):
        # remote server client
        self.server.clients.remove(self)
        # close connection
        self.close()

        # log disconnection
        logger.info("Client [%s] disconnected." % (
            self.address))

class Client(Dispatcher):
    def __init__(self, server, sock):
        # initialize dispatcher
        Dispatcher.__init__(self, sock)

        # assign instance properties
        self.server = server 
        self.player = None

        # greet player
        self.write("Welcome to the MUD!")
        self.prompt("Please enter your name: ", self.connect)

    def connect(self, name):
        # require character name
        if not name:
            self.write("Character name required. Disconnecting...")
            self.close()

        #self.write("Character creation currently disabled. Sorry!")
        #self.disconnect()

        # initialize player
        self.player = Player(self, name)
        self.player.init()

    def read(self):
        # read data from dispatcher
        data = Dispatcher.read(self)                
        # return if player is not authenticated
        if not self.player.authed: return
        # return prompt if no data was returned
        if not data: 
            self.write_prompt()
            return

        # split data by words
        words = data.strip().split(' ')
        # return if no human readable input was found
        if not words: 
            self.write_prompt("What?")
            return

        # determine command
        command = words[0].lower()
        # attempt to import command module
        try:
            module = importlib.import_module('commands.%s' % command)
        except ImportError:
            self.write_prompt("What?")
            return
        # determine command class object
        module = getattr(module, command, None)
        if not module:
            logger.error("Command module '%s' found but no class defined!" % command)
            self.write_prompt("What?")
            return
        # initialize command
        command = module(self.player)
        # execute command
        command(' '.join(words[1:]))
        # output player prompt
        self.write_prompt()

        # # TODO: working
        # line = self.chat.get_line(words[0])
        # if line: # and Player.level >= chat_line[0][0]
        #     self.chat.send(line[0][1], ' '.join(words[1:]))
        # # TODO: end working

    def write_prompt(self, msg=None):
        # output message if requested
        if msg: self.write(msg)
        # output player prompt
        self.write(self.player.prompt, False)        
