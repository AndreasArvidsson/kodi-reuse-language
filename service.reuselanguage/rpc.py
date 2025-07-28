import json
import xbmc
from my_types import CurrentProperties, StreamsProperties

player_id = 1


def rpc_get_current() -> CurrentProperties:
    return rpc(
        "Player.GetProperties",
        {
            "playerid": player_id,
            "properties": [
                "subtitleenabled",
                "currentaudiostream",
                "currentsubtitle",
            ],
        },
    )


def rpc_get_streams() -> StreamsProperties:
    return rpc(
        "Player.GetProperties",
        {
            "playerid": player_id,
            "properties": [
                "audiostreams",
                "subtitles",
            ],
        },
    )


def rpc_set_audio_stream(index):
    rpc(
        "Player.SetAudioStream",
        {
            "playerid": player_id,
            "stream": index,
        },
    )


def rpc_set_subtitle(index):
    rpc(
        "Player.SetSubtitle",
        {
            "playerid": player_id,
            "subtitle": index,
            "enable": True,
        },
    )


def rpc_disable_subtitle():
    rpc(
        "Player.SetSubtitle",
        {
            "playerid": player_id,
            "subtitle": "off",
            "enable": False,
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
