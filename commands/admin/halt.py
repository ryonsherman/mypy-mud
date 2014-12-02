from commands import Command

class halt(Command):
    def __call__(self):
        # return if player is not admin
        if not self.player.admin: return
        # stop server
        self.player.client.server.stop()
