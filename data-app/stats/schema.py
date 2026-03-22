from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime


Binary = Literal[0, 1]


class PredictRow(BaseModel):
    player_id: str
    player_name: str
    team_id: str
    team: str
    opponent_id: str
    opponent: str
    is_home: Binary
    avg_minutes: int
    started: int = 1


class BuildModelRow(BaseModel):
    player_id: str
    team_id: str
    opponent_id: str
    stat: float
    is_home: Binary
    started: Binary
    min: int = Field(gt=0)
    date: datetime
