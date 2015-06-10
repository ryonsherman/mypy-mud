#!/usr/bin/env python2

__author__    = "Ryon Sherman"
__email__     = "ryon.sherman@gmail.com"
__copyright__ = "Copyright 2015, Ryon Sherman"
__license__   = "MIT"

import threading

from log import log


class Console(object):
    def __init__(self, server):
        self.server = server
        self.prompt = 'mud'

    @property
    def prompt(self):
        return getattr(self, '_prompt', '> ')

    @prompt.setter
    def prompt(self, prompt):
        self._prompt = prompt.lstrip(' ').lstrip('>') + '> '

    def command(self, cmd, *args):
        cmd = getattr(self, cmd, None)
        if not cmd or not callable(cmd): return None
        cmd(*args)

    def start(self):
        thread = getattr(self, '_thread', None)
        if thread and thread.isAlive(): return
        self._thread = threading.Thread(target=self.server.start)
        self._thread.start()

    def stop(self):
        thread = getattr(self, '_thread', None)
        if not thread or not thread.isAlive(): return
        self.server.stop()
        self._thread.join()

    def who(self):
        if not self.server.connected: return
        print 'who'