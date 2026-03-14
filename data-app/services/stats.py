from schemas import Field, League
from sqlalchemy import case, select, func, cast, Float
from sqlalchemy.orm import Session
from models import PlayerMatchReport, Match, Team, Player
from stats.schema import BuildModelRow, PredictRow
from crud.player_match_report import get_avg_minutes_played_when_started
from crud.team import get_or_create_team
from fbref.schema import Match as FbrefMatch
from collections import defaultdict

FIELD_COLUMN_MAP = {
    Field.SH: PlayerMatchReport.sh,
    Field.SOT: PlayerMatchReport.sot,
    Field.FLS: PlayerMatchReport.fls,
    Field.FLD: PlayerMatchReport.fld,
}


def build_model_rows(
    session: Session,
    league: League,
    field: Field,
) -> list[BuildModelRow]:
    stat_col = FIELD_COLUMN_MAP.get(field)
    if stat_col is None:
        raise ValueError(f"No column mapping found for field '{field}'.")

    opponent_id = case(
        (PlayerMatchReport.team_id == Match.home_team_id, Match.away_team_id),
        else_=Match.home_team_id,
    ).label("opponent_id")

    is_home = (PlayerMatchReport.team_id == Match.home_team_id).label("is_home")

    stmt = (
        select(
            PlayerMatchReport.player_id,
            PlayerMatchReport.team_id,
            PlayerMatchReport.started,
            PlayerMatchReport.min,
            stat_col.label("stat"),
            Match.date,
            opponent_id,
            is_home,
        )
        .join(Match, PlayerMatchReport.match_id == Match.id)
        .join(Team, PlayerMatchReport.team_id == Team.id)
        .where(Team.league == league)
        # exclude reports where player has played less than 15 minutes
        .where(PlayerMatchReport.min > 15)
    )

    rows = session.execute(stmt).all()

    player_mins_map = defaultdict(int)

    for row in rows:
        player_mins_map[row.player_id] += row.min

    model_rows = [
        BuildModelRow(
            player_id=str(row.player_id),
            team_id=str(row.team_id),
            opponent_id=str(row.opponent_id),
            stat=float(row.stat),
            is_home=int(row.is_home),
            started=int(row.started),
            min=row.min,
            date=row.date,
        )
        for row in rows
        #  exclude players who haven't played 5 games worth of football
        if player_mins_map[row.player_id] > 450
    ]

    return model_rows


def get_current_players(session: Session, team_id: str) -> list[Player]:
    # Subquery: find the latest match_id for each player
    latest_match_subq = (
        select(
            PlayerMatchReport.player_id,
            func.max(Match.date).label("latest_date"),
        )
        .join(Match, PlayerMatchReport.match_id == Match.id)
        .group_by(PlayerMatchReport.player_id)
        .subquery()
    )

    # Subquery: get the team_id from that latest match report
    latest_report_subq = (
        select(PlayerMatchReport.player_id, PlayerMatchReport.team_id)
        .join(Match, PlayerMatchReport.match_id == Match.id)
        .join(
            latest_match_subq,
            (PlayerMatchReport.player_id == latest_match_subq.c.player_id)
            & (Match.date == latest_match_subq.c.latest_date),
        )
        .subquery()
    )

    # Main query: find all players whose latest match was for the given team
    stmt = (
        select(Player)
        .join(latest_report_subq, Player.id == latest_report_subq.c.player_id)
        .where(latest_report_subq.c.team_id == team_id)
    )

    return session.scalars(stmt).all()


def build_predict_rows(session: Session, match: FbrefMatch) -> list[PredictRow]:
    home_team = get_or_create_team(session, match.home_team, match.league)
    home_players = get_current_players(session, home_team.id)

    away_team = get_or_create_team(session, match.away_team, match.league)
    away_players = get_current_players(session, away_team.id)

    rows: list[PredictRow] = []

    for player in home_players:
        avg_minutes = get_avg_minutes_played_when_started(
            session, player.id, match.season
        )
        row = PredictRow(
            player_id=str(player.id),
            player_name=player.name,
            team_id=str(home_team.id),
            opponent_id=str(away_team.id),
            is_home=1,
            started=1,
            avg_minutes=int(avg_minutes),
        )
        rows.append(row)

    for player in away_players:
        avg_minutes = get_avg_minutes_played_when_started(
            session, player.id, match.season
        )
        row = PredictRow(
            player_id=str(player.id),
            player_name=player.name,
            team_id=str(away_team.id),
            opponent_id=str(home_team.id),
            is_home=0,
            started=1,
            avg_minutes=int(avg_minutes),
        )
        rows.append(row)

    return rows


def get_dispersion_by_league(session: Session, league: League, field: Field):
    col = FIELD_COLUMN_MAP[field]
    avg_val = func.avg(col)
    var_val = func.variance(col)

    selections = [
        avg_val.label(f"mean_{field}"),
        var_val.label(f"var_{field}"),
        (var_val / avg_val).label(f"dispersion_{field}"),
    ]

    stmt = (
        select(*selections)
        .join(Team, PlayerMatchReport.team_id == Team.id)
        .where(Team.league == league)
        .where(PlayerMatchReport.min >= 60)
    )

    return session.execute(stmt).first()
