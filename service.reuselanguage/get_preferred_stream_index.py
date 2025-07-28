from typing import List
from my_types import PlayerStream


def get_preferred_stream_index(
    streams: List[PlayerStream],
    previous_stream: PlayerStream,
):
    language = previous_stream["language"]
    name = previous_stream["name"]
    index = previous_stream["index"]

    # Only match streams with the same language
    streams = [s for s in streams if s["language"] == language]

    # 1) Try to match: language, name and index
    matched_streams = [s for s in streams if s["name"] == name and s["index"] == index]

    # 2) Try to match: language and name
    if not matched_streams:
        matched_streams = [s for s in streams if s["name"] == name]

    # 3) Try to match: language and isdefault
    if not matched_streams:
        matched_streams = [s for s in streams if s["isdefault"]]

    # 4) Try to match: language
    if not matched_streams:
        matched_streams = streams

    if not matched_streams:
        return -1

    return matched_streams[0]["index"]
