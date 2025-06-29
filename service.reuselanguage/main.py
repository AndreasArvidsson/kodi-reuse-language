from typing import Optional
from my_types import PlayerProperties
from rpc import get_properties, set_audio_stream, set_subtitle
from util import get_preferred_stream_index
import xbmc


def log(message: str):
    xbmc.log(f"[ReuseLanguage] {message}", level=xbmc.LOGINFO)


class PlayerMonitor(xbmc.Player):
    monitor: xbmc.Monitor
    do_updates: bool
    properties: Optional[PlayerProperties]

    def __init__(self):
        super().__init__()
        self.monitor = xbmc.Monitor()
        self.properties = None
        self.do_updates = False

    def onAVStarted(self):
        if not self.isPlayingVideo():
            return
        log("Playback started")
        self.set_streams()
        self.do_updates = True

    def onPlayBackStopped(self):
        log("Playback stopped")
        self.do_updates = False

    def onPlayBackEnded(self):
        log("Playback ended")
        self.do_updates = False

    def run(self):
        while not self.monitor.abortRequested():
            if self.do_updates:
                self.properties = get_properties()
            # 1 second polling
            xbmc.sleep(1000)

    def set_streams(self):
        if not self.properties:
            return
        properties = get_properties()
        audio_index = get_preferred_stream_index(
            properties["audiostreams"],
            self.properties["currentaudiostream"],
        )
        if audio_index > -1:
            log(f"Setting audio stream to {audio_index}")
            set_audio_stream(audio_index)

        if not self.properties["subtitleenabled"]:
            return
        subtitle_index = get_preferred_stream_index(
            properties["subtitles"],
            self.properties["currentsubtitle"],
        )
        if subtitle_index > -1:
            log(f"Setting subtitle stream to {subtitle_index}")
            set_subtitle(subtitle_index)


if __name__ == "__main__":
    xbmc.log("[LanguageControl] Addon started", level=1)
    player = PlayerMonitor()
    player.run()
    xbmc.log("[LanguageControl] Addon stopped", level=1)
