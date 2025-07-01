from player import Player
import xbmc


if __name__ == "__main__":
    monitor = xbmc.Monitor()
    player = Player()

    while not monitor.abortRequested():
        if monitor.waitForAbort(10):
            break
        player.update()
