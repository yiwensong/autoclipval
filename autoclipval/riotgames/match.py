import typing

import attr


@attr.s(auto_attribs=True)
class MatchInfo:
    match_id: str
    map_id: str
    game_length_millis: int
    game_start_millis: float
    provisioning_flow_id: str
    is_complete: bool
    queue_id: str
    game_mode: str
    is_ranked: bool
    season_id: str


@attr.s(auto_attribs=True)
class Match:
    match_info: MatchInfo
    players: typing.List[Player]
    coaches: typing.List[Coach]
    teams: typing.List[Team]
    round_results: typing.List[RoundResult]


@attr.s(auto_attribs=True)
class Player:
    puuid: str
    game_name: str
    tag_line: str
    team_id: str
    party_id: str
    character_id: str
    stats: PlayerStats
    competitive_tier: int
    player_card: str
    player_title: str


@attr.s(auto_attribs=True)
class PlayerStats:
    score: int
    rounds_played: int
    kills: int
    deaths: int
    assists: int
    playtime_millis: int
    ability_casts: AbilityCasts


@attr.s(auto_attribs=True)
class AbilityCasts:
    grenade_casts: int
    ability1_casts: int
    ability2_casts: int
    ultimate_casts: int


@attr.s(auto_attribs=True)
class Coach:
    puuid: str
    team_id: str


@attr.s(auto_attribs=True)
class Team:
    team_id: str
    won: bool
    rounds_played: int
    rounds_won: int
    num_points: int
    

@attr.s(auto_attribs=True)
class RoundResult:
    round_num: int
    round_result: str
    round_ceremony: str
    winning_team: str
    bomb_planter: str
    bomb_defuser: str
    plant_round_time: int
    plant_player_locations: typing.List[PlayerLocation]
    plant_location: Location
    plant_site: str
    defuse_round_time: int
    defuse_player_locations: typing.List[PlayerLocation]
    player_stats: typing.List[PlayerRoundStats]
    round_result_code: str


@attr.s(auto_attribs=True)
class PlayerLocation:
    puuid: str
    view_radians: float
    location: Location


@attr.s(auto_attribs=True)
class Location:
    x: int
    y: int


@attr.s(auto_attribs=True)
class PlayerRoundStats:
    puuid: str
    kills: typing.List[Kill]
    damage: typing.List[Damage]
    score: int
    economy: Economy
    ability: Ability

@attr.s(auto_attribs=True)
class Kill:
    time_since_game_start_millis: int
    time_since_round_start_millis: int
    killer: str
    victim: str
    victim_location: Location
    assistants: typing.List[str]
    player_locations: typing.List[PlayerLocation]
    finishing_damage: FinishingDamage

@attr.s(auto_attribs=True)
class FinishingDamage:
    damage_type: string
    damage_item: string
    is_secondary_fire_mode: bool


@attr.s(auto_attribs=True)
class Damage:
    receiver: str
    damage: int
    legshots: int
    bodyshots: int
    headshots: int


@attr.s(auto_attribs=True)
class Economy:
    loadout_value: int
    weapon: str
    armor: str
    remaining: int
    spent: int


@attr.s(auto_attribs=True)
class Ability:
    grenade_effects: str
    ability1_effects: str
    ability2_effects: str
    ultimate_effects: str
