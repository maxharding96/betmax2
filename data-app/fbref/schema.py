from pydantic import BaseModel
from schemas import Match


class MatchReport(BaseModel):
    player: str
    started: bool
    min: int
    sh: int
    sot: int
    fls: int
    fld: int


class MatchWithReports(Match):
    home_reports: list[MatchReport]
    away_reports: list[MatchReport]
