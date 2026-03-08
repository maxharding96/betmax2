from sqlalchemy.orm import Session
from fbref.schema import MatchWithReports, MatchReport
from crud.team import get_or_create_team
from crud.match import get_or_create_match
from crud.player import get_or_create_player
from crud.player_match_report import create_many_reports
from models import PlayerMatchReport


def create_player_match_report(
    session: Session, fbref_report: MatchReport, match_id: int, team_id: int
) -> PlayerMatchReport:
    player = get_or_create_player(session, player_name=fbref_report.player)

    return PlayerMatchReport(
        player_id=player.id,
        match_id=match_id,
        team_id=team_id,
        started=fbref_report.started,
        min=fbref_report.min,
        sh=fbref_report.sh,
        sot=fbref_report.sot,
        fls=fbref_report.fls,
        fld=fbref_report.fld,
    )


def create_fbref_match(session: Session, fbref_match: MatchWithReports):
    league = fbref_match.league
    season = fbref_match.season

    home_team = get_or_create_team(
        session, team_name=fbref_match.home_team, league=league
    )
    away_team = get_or_create_team(
        session, team_name=fbref_match.away_team, league=league
    )

    match = get_or_create_match(
        session,
        season=season,
        home_team_id=home_team.id,
        away_team_id=away_team.id,
        date=fbref_match.date,
    )

    reports_to_create: list[PlayerMatchReport] = []

    for fbref_report in fbref_match.home_reports:
        report = create_player_match_report(
            session, fbref_report, match_id=match.id, team_id=home_team.id
        )
        reports_to_create.append(report)

    for fbref_report in fbref_match.away_reports:
        report = create_player_match_report(
            session, fbref_report, match_id=match.id, team_id=away_team.id
        )
        reports_to_create.append(report)

    create_many_reports(session, reports_to_create)

    session.commit()
