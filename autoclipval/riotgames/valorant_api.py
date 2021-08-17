import os
import typing

import requests

API_KEY = ""
API_BASE_URL = "https://americas.api.riotgames.com"


def get_api_key() -> str:
    """Gets the api key from environment variable. In the future, this
    can be extended to also get from disk or something."""
    API_KEY = os.environ.get("RIOT_API_KEY", "")
    return API_KEY


class RiotClientException(Exception):
    pass


def get_puuid(game_name: str, tag_line: str) -> str:
    """Converts a game name tag line combo into a puuid that the riot
    api understands."""
    accounts_route = (
        f"riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    )
    resp = requests.get(
        f"{API_BASE_URL}/{accounts_route}",
        headers={
            "X-Riot-Token": API_KEY,
        },
    )
    if resp.code != requests.codes.ok:
        raise RiotClientException(resp.text)

    player = resp.json()
    puuid = player.get("puuid")

    if puuid == "":
        raise RiotClientException(
            "puuid was not found in player response: {player}",
        )

    return puuid


def get_last_match_id(puuid: str) -> str:
    """Returns the last played match id for a user."""
    match_list_route = f"val/match/v1/matchlist/by-puuid/{puuid}"
    resp = requests.get(
        f"{API_BASE_URL}/{match_list_route}",
        headers={
            "X-Riot-Token": API_KEY,
        },
    )
    if resp.code != requests.codes.ok:
        raise RiotClientException(resp.text)

    matchlist = resp.json()
    history = matchlist["history"]

    if len(history) == 0:
        raise RiotClientException(f"no matches found for {puuid}")

    last_match_id = history[-1]["matchId"]

    return last_match_id


# TODO: these should respond with the python types rather than the
# dicts if possible. but we can deal with that later.
def get_match_by_id(match_id: str) -> typing.Dict[str, typing.Any]:
    """Returns the results of a match id."""
    match_route = f"val/match/v1/matches/{match_id}"
    resp = requests.get(
        f"{API_BASE_URL}/{match_route}",
        headers={
            "X-Riot-Token": API_KEY,
        },
    )
    if resp.code != requests.codes.ok:
        raise RiotClientException(resp.text)

    match = resp.json()
    return match


def get_last_match(
    game_name: str,
    tag_line: str,
) -> typing.Dict[str, typing.Any]:
    """Returns the last match info for a user."""
    puuid = get_uuid(game_name, tag_line)
    match_id = get_last_match_id(puuid)
    return get_last_match_id(match_id)


@attr.s(auto_attribs=True)
class Event:
    """A game event"""
    timestamp: float
    event_type: str
    event_desc: str


def get_match_events(
    match: typing.Dict[str, typing.Any],
    puuid: str,
) -> typing.List[Event]:
    """Returns a list of game events relevant for a player."""
    events: typing.List[Event] = []
    game_start = match["matchInfo"]["gameStartMillis"]
    rounds = match.get("roundResults", [])
    for rd in rounds:
        player_stats = rd["playerStats"]
        for k in player_stats["kills"]:
            timestamp = game_start + k["timeSinceGameStartMillis"]
            if k["killer"] == puuid:
                event_type = "kill"
            elif k["victim"] == puuid:
                event_type = "death"
            elif puuid in k["assistants"]:
                event_type = "assist"
            else:
                # User is not part of this event
                continue
            event = Event(
                timestamp=timestamp,
                event_type=event_type,
                event_desc="",
            )
            events.append(event)
    return events
