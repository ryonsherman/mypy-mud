#!/usr/bin/env python2

__author__    = "Ryon Sherman"
__email__     = "ryon.sherman@gmail.com"
__copyright__ = "Copyright 2014, Ryon Sherman"
__license__   = "MIT"

from commands import Command


class quit(Command):
    def __call__(self, *args):
        # save player
        self.player.save()
        # goodbye player
        self.player.client.write("Goodbye.")
        # quit player
        self.player.client.close()
