from schemas import PredictionField, League
from sqlalchemy import case, select
from sqlalchemy.orm import Session
from models import PlayerMatchReport, Match, Team
from stats.schema import BuildModelRow

FIELD_COLUMN_MAP = {
    PredictionField.SH: PlayerMatchReport.sh,
    PredictionField.SOT: PlayerMatchReport.sot,
    PredictionField.FLS: PlayerMatchReport.fls,
    PredictionField.FLD: PlayerMatchReport.fld,
}


def build_model_rows(
    session: Session,
    league: League,
    field: PredictionField,
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
            PlayerMatchReport.started,
            PlayerMatchReport.min.label("minutes"),
            stat_col.label("stat"),
            Match.date,
            opponent_id,
            is_home,
        )
        .join(Match, PlayerMatchReport.match_id == Match.id)
        .join(Team, PlayerMatchReport.team_id == Team.id)
        .where(Team.league == league)
        .where(PlayerMatchReport.min > 0)
    )

    rows = session.execute(stmt).all()

    return [
        BuildModelRow(
            player_id=str(row.player_id),
            opponent_id=str(row.opponent_id),
            stat=float(row.stat),
            is_home=int(row.is_home),
            started=int(row.started),
            min=row.min,
            date=row.date,
        )
        for row in rows
    ]
