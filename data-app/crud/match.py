from models import Match
from sqlalchemy import select
from sqlalchemy.orm import Session
from schemas import Season
from datetime import datetime


def get_or_create_match(
    session: Session,
    season: Season,
    home_team_id: int,
    away_team_id: int,
    date: datetime,
):
    """Checks if match exists; if not, creates it."""
    stmt = select(Match).where(
        Match.season == season,
        Match.home_team_id == home_team_id,
        Match.away_team_id == away_team_id,
    )
    match = session.execute(stmt).scalar_one_or_none()

    if not match:
        match = Match(
            season=season,
            home_team_id=home_team_id,
            away_team_id=away_team_id,
            date=date,
        )
        session.add(match)
        session.flush()

    return match
