from pydantic import BaseModel
from schemas import League, Season
from datetime import datetime


class MatchReport(BaseModel):
    player: str
    started: bool
    min: int
    sh: int
    sot: int
    fls: int
    fld: int


class Match(BaseModel):
    league: League
    season: Season
    home_team: str
    away_team: str
    date: datetime


class MatchWithReports(Match):
    home_reports: list[MatchReport]
    away_reports: list[MatchReport]
