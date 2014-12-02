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
        # inform players of player departure
        self.player.client.server.inform(self.player.client,
            "%s has left the MUD." % self.player.name)
        # remove client session
        del self.player.client.server.sessions[self.player.uuid]
        # quit player
        self.player.client.close()
