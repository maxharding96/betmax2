from sqlalchemy.orm import Session
from sqlalchemy import select, func
from models import PlayerMatchReport, Match
from schemas import Season


def create_many_reports(session: Session, reports: list[PlayerMatchReport]):
    session.add_all(reports)
    session.commit()

    for report in reports:
        session.refresh(report)

    return reports


def get_avg_minutes_played_when_started(
    session: Session, player_id: int, season: Season
) -> float:
    stmt = (
        select(func.avg(PlayerMatchReport.min))
        .join(Match, Match.id == PlayerMatchReport.match_id)
        .where(Match.season == season)
        .where(PlayerMatchReport.player_id == player_id)
        .where(PlayerMatchReport.started)
    )

    return session.execute(stmt).scalar() or 0
