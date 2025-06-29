import xbmc
import json
from my_types import PlayerProperties

player_id = 1


def get_properties() -> PlayerProperties:
    return rpc(
        "Player.GetProperties",
        {
            "playerid": 1,
            "properties": [
                "subtitleenabled",
                "currentaudiostream",
                "currentsubtitle",
                "audiostreams",
                "subtitles",
            ],
        },
    )


def set_audio_stream(stream_index):
    rpc(
        "Player.SetAudioStream",
        {
            "playerid": player_id,
            "stream": stream_index,
        },
    )


def set_subtitle(subtitle_index):
    rpc(
        "Player.SetSubtitle",
        {
            "playerid": player_id,
            "subtitle": subtitle_index,
            "enable": True,
        },
    )


def rpc(method: str, params: dict):
    payload = xbmc.executeJSONRPC(
        json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": method,
                "params": params,
            }
        )
    )
    return json.loads(payload).get("result", {})
