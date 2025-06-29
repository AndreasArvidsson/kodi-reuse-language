from typing import List, TypedDict


class PlayerStream(TypedDict):
    index: int
    language: str
    name: str
    isdefault: bool


class PlayerProperties(TypedDict):
    subtitleenabled: bool
    currentaudiostream: PlayerStream
    currentsubtitle: PlayerStream
    audiostreams: List[PlayerStream]
    subtitles: List[PlayerStream]
