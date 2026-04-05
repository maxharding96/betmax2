from models import Team
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_or_create_team(session: Session, team_name: str) -> Team:
    """Checks if team exists by name; if not, creates it."""
    stmt = select(Team).where(Team.name == team_name)
    team = session.execute(stmt).scalar_one_or_none()

    if not team:
        team = Team(name=team_name)
        session.add(team)
        session.flush()

    return team
