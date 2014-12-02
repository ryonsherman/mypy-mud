from commands import Command

class reboot(Command):
    def __call__(self):
        # return if player is not admin
        if not self.player.admin: return
        # reboot server
        self.player.client.server.restart()
