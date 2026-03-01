from models import Player
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_or_create_player(session: Session, player_name: str) -> Player:
    """Checks if team exists by name; if not, creates it."""
    stmt = select(Player).where(Player.name == player_name)
    player = session.execute(stmt).scalar_one_or_none()

    if not player:
        player = Player(name=player_name)
        session.add(player)
        session.flush()

    return player
