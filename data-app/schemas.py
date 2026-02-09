from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
import enum


class League(enum.IntEnum):
    PREMIER_LEAGUE = 0
    CHAMPIONSHIP = 1


class Season(enum.IntEnum):
    S_23 = 0
    S_24 = 1
    S_25 = 2


class PredictionField(enum.IntEnum):
    SH = 0
    SOT = 1


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TeamBase(BaseSchema):
    id: int
    name: str
    league: League


class PlayerBase(BaseSchema):
    id: int
    name: str
    team_id: int


class Player(PlayerBase):
    team: Optional[TeamBase] = None


class MatchBase(BaseSchema):
    id: int
    match_day: int
    date: datetime
    season: Season
    # Nullable coefficients
    home_attack_coeffs: Optional[float] = None
    away_attack_coeffs: Optional[float] = None
    home_defence_coeffs: Optional[float] = None
    away_defence_coeffs: Optional[float] = None
    # FK IDs (Raw integers)
    home_team_id: int
    away_team_id: int


class Match(MatchBase):
    # Nested Relationships
    home_team: Optional[TeamBase] = None
    away_team: Optional[TeamBase] = None


class MatchReportBase(BaseSchema):
    id: int
    started: bool
    min: int
    sh: int
    sot: int
    fls: int
    fld: int
    # FK IDs
    match_id: int
    player_id: int


class MatchReport(MatchReportBase):
    match: Optional[MatchBase] = None
    player: Optional[PlayerBase] = None


class MatchPredictionBase(BaseSchema):
    id: int
    field: PredictionField
    value: float
    # FK IDs
    match_id: int
    player_id: int


class MatchPrediction(MatchPredictionBase):
    match: Optional[MatchBase] = None
    player: Optional[PlayerBase] = None
