from sqlalchemy.orm import Session
from models import PlayerMatchReport


def create_many_reports(session: Session, reports: list[PlayerMatchReport]):
    session.add_all(reports)
    session.commit()

    for report in reports:
        session.refresh(report)

    return reports
