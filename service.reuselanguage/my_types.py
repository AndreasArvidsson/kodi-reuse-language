from typing import List, TypedDict


class PlayerStream(TypedDict):
    index: int
    language: str
    name: str
    isdefault: bool


class CurrentProperties(TypedDict):
    subtitleenabled: bool
    currentaudiostream: PlayerStream
    currentsubtitle: PlayerStream


class StreamsProperties(TypedDict):
    audiostreams: List[PlayerStream]
    subtitles: List[PlayerStream]
