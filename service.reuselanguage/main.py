import xbmc
from player import Player

if __name__ == "__main__":
    monitor = xbmc.Monitor()
    player = Player()

    while not monitor.abortRequested():
        if monitor.waitForAbort(10):
            break
        player.update()
