from pydantic import BaseModel
from schemas import Field
from fbref.schema import Match


class Odds(BaseModel):
    point: float
    player: str
    value: str


class FieldOdds(BaseModel):
    field: Field
    odds: list[Odds]


class MatchOdds(BaseModel):
    match: Match
    fields_odds: list[FieldOdds]
