from pydantic import BaseModel
from schemas import Field
from fbref.schema import Match


class Odds(BaseModel):
    point: float
    player: str
    value: str


class MatchOdds(BaseModel):
    match: Match
    field_to_odds: dict[Field, list[Odds]]
