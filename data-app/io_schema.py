from pydantic import BaseModel
from schemas import Field, League, Match
from typing import Literal


class GetRowsInput(BaseModel):
    match: Match
    field: Field
    over: float


class Row(BaseModel):
    player: str
    team: str
    opponent: str
    venue: Literal["home", "away"]
    odds: str
    prediction: float


class GetRowsOutput(BaseModel):
    rows: list[Row]


class GetMatchesInput(BaseModel):
    league: League


class GetMatchesOutput(BaseModel):
    matches: list[Match]
