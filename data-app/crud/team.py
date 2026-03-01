from models import Team
from schemas import League
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_or_create_team(session: Session, team_name: str, league: League) -> Team:
    """Checks if team exists by name; if not, creates it."""
    stmt = select(Team).where(Team.name == team_name)
    team = session.execute(stmt).scalar_one_or_none()

    if not team:
        team = Team(name=team_name, league=league)
        session.add(team)
        session.flush()

    return team
