import os
import typing

import requests

API_KEY = ""
API_BASE_URL = "https://api.twitch.tv"


class TwitchClientException(Exception):
    pass


def create_clip(broadcaster_id: str, has_delay: bool) -> None:
    clip_route = "helix/clips"
    resp = requests.post(
        f"{API_BASE_URL}/{clip_route}",
        data={
            broadcaster_id: broadcaster_id,
            has_delay: has_delay,
        },
        headers={
            "Authorization": f"OAuth {API_KEY}",
        },
    )
    if resp.code != requests.codes.ok:
        raise TwitchClientException(
            f"Twitch returned an unexpected response: {resp.text}",
        )
