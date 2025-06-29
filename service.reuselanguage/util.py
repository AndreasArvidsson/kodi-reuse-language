from typing import List
from my_types import PlayerStream


def get_preferred_stream_index(
    streams: List[PlayerStream], previous_stream: PlayerStream
):
    language = previous_stream["language"]
    name = previous_stream["name"]

    # First try to match both language and name
    matched_streams = [
        stream
        for stream in streams
        if stream["language"] == language and stream["name"] == name
    ]

    # Secondly, try to match default stream for language
    if not matched_streams:
        matched_streams = [
            stream
            for stream in streams
            if stream["language"] == language and stream["isdefault"]
        ]

    # Finally, try to match only by language
    if not matched_streams:
        matched_streams = [
            stream for stream in streams if stream["language"] == language
        ]

    if not matched_streams:
        return -1

    return matched_streams[0]["index"]
