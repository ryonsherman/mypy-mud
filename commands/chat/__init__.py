#!/usr/bin/env python2

__author__    = "Ryon Sherman"
__email__     = "ryon.sherman@gmail.com"
__copyright__ = "Copyright 2014, Ryon Sherman"
__license__   = "MIT"

from commands import Command


class chat(Command):
    lines = {
        0: 'newbie',
        10: 'mid',
        20: 'hm',
        50: 'elite', 
        100: 'legend'
    }

    def __call__(self, msg):
        self.send('newbie', msg)

        # parts = msg.split(' ')
        # if len(parts) < 2:
        #     # todo: need message
        #     pass
        # line, msg = parts[0], ' '.join(parts[1:])
        # print 'chatting %s on %s' % (msg, line)

    def get_line(self, line):
        # ensure lowercase line index
        line = line.lower()
        # return line if found
        return filter(lambda x: x[1] == line, self.lines.items())

    def send(self, line, msg):
        msg = "%s <%s> %s" % (self.player.name, line, msg.strip())
        for client in self.player.client.server.clients:
            client.write(msg)
