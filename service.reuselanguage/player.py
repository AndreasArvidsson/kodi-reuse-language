from typing import Optional

import xbmc
from my_types import CurrentProperties, PlayerStream
from rpc import (
    rpc_disable_subtitle,
    rpc_get_current,
    rpc_get_streams,
    rpc_set_audio_stream,
    rpc_set_subtitle,
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
    audiostreams: list[PlayerStream],
    currentaudiostream: PlayerStream,
):
    if not currentaudiostream:
        return

    audio_index = get_preferred_stream_index(audiostreams, currentaudiostream)

    if audio_index > -1:
        rpc_set_audio_stream(audio_index)


def set_subtitle(
    subtitles: list[PlayerStream],
    currentsubtitle: PlayerStream,
    subtitleenabled: bool,
):
    if not subtitleenabled:
        rpc_disable_subtitle()
        return

    if not currentsubtitle:
        return

    subtitle_index = get_preferred_stream_index(subtitles, currentsubtitle)

    if subtitle_index > -1:
        rpc_set_subtitle(subtitle_index)
