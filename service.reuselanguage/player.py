from typing import List, Optional

import xbmc
from get_preferred_stream_index import get_preferred_stream_index
from my_types import CurrentProperties, PlayerStream
from rpc import (
    rpc_disable_subtitle,
    rpc_get_current,
    rpc_get_streams,
    rpc_set_audio_stream,
    rpc_set_subtitle,
)


class Player(xbmc.Player):
    do_updates: bool
    stored: Optional[CurrentProperties]

    def __init__(self):
        super().__init__()
        self.do_updates = False
        self.stored = None

    def onAVStarted(self):
        if self.isPlayingVideo():
            if self.stored:
                set_streams(self.stored)
            self.do_updates = True

    def onPlayBackStopped(self):
        self.do_updates = False

    def onPlayBackEnded(self):
        self.do_updates = False

    def update(self):
        if self.do_updates:
            self.stored = rpc_get_current()


def set_streams(stored: CurrentProperties):
    streams = rpc_get_streams()

    set_audio_stream(
        streams["audiostreams"],
        stored["currentaudiostream"],
    )
    set_subtitle(
        streams["subtitles"],
        stored["currentsubtitle"],
        stored["subtitleenabled"],
    )


def set_audio_stream(
    audiostreams: List[PlayerStream],
    currentaudiostream: PlayerStream,
):
    audio_index = get_preferred_stream_index(audiostreams, currentaudiostream)

    if audio_index > -1:
        rpc_set_audio_stream(audio_index)


def set_subtitle(
    subtitles: List[PlayerStream],
    # Optional is not technically true: if not set this will be an empty dictionary.
    currentsubtitle: Optional[PlayerStream],
    subtitleenabled: bool,
):
    # Previously stored properties had no subtitle
    if not currentsubtitle or not subtitleenabled:
        rpc_disable_subtitle()
        return

    subtitle_index = get_preferred_stream_index(subtitles, currentsubtitle)

    if subtitle_index > -1:
        rpc_set_subtitle(subtitle_index)
