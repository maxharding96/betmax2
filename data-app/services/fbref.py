from sqlalchemy.orm import Session
from fbref.schema import Match
from crud.team import get_or_create_team
from crud.match import get_or_create_match
from crud.player import get_or_create_player
from crud.player_match_report import create_many_reports
from models import PlayerMatchReport


def create_fbref_match(session: Session, fbref_match: Match):
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

    fbref_reports = fbref_match.home_reports + fbref_match.away_reports

    for fbref_report in fbref_reports:
        player = get_or_create_player(session, player_name=fbref_report.player)

        report = PlayerMatchReport(
            player_id=player.id,
            match_id=match.id,
            team_id=home_team.id,
            started=fbref_report.started,
            min=fbref_report.min,
            sh=fbref_report.sh,
            sot=fbref_report.sot,
            fls=fbref_report.fls,
            fld=fbref_report.fld,
        )

        reports_to_create.append(report)

    create_many_reports(session, reports_to_create)

    session.commit()
