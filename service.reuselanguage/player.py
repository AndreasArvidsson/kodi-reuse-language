from typing import Optional

import xbmc
from my_types import CurrentProperties
from rpc import (
    disable_subtitle,
    get_current,
    get_streams,
    set_audio_stream,
    set_subtitle,
)
from util import get_preferred_stream_index


class Player(xbmc.Player):
    do_updates: bool
    stored: Optional[CurrentProperties]

    def __init__(self):
        super().__init__()
        self.do_updates = False
        self.stored = None

    def onAVStarted(self):
        if self.isPlayingVideo():
            self.set_streams()
            self.do_updates = True

    def onPlayBackStopped(self):
        self.do_updates = False

    def onPlayBackEnded(self):
        self.do_updates = False

    def update(self):
        if self.do_updates:
            self.stored = get_current()

    def set_streams(self):
        if not self.stored:
            return

        streams = get_streams()

        audio_index = get_preferred_stream_index(
            streams["audiostreams"],
            self.stored["currentaudiostream"],
        )

        if audio_index > -1:
            set_audio_stream(audio_index)

        if not self.stored["subtitleenabled"]:
            disable_subtitle()
            return

        subtitle_index = get_preferred_stream_index(
            streams["subtitles"],
            self.stored["currentsubtitle"],
        )

        if subtitle_index > -1:
            set_subtitle(subtitle_index)
