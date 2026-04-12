from schemas import Field, League
from sqlalchemy import case, select, func
from sqlalchemy.orm import Session
from models import PlayerMatchReport, Match, Team, Player
from .schema import BuildModelRow, PredictRow
from fbref.schema import Match as FbrefMatch, MatchWithReports, MatchReport
from collections import defaultdict
from crud.match import get_or_create_match
from crud.team import get_or_create_team
from crud.player import get_or_create_player
from crud.player_match_report import (
    create_many_reports,
    get_avg_minutes_played_when_started,
)
from .player_model import PlayerModel
from database import get_session
from odds.schema import Odds
import difflib
import io_schema as io


FIELD_COLUMN_MAP = {
    Field.SH: PlayerMatchReport.sh,
    Field.SOT: PlayerMatchReport.sot,
    Field.FLS: PlayerMatchReport.fls,
    Field.FLD: PlayerMatchReport.fld,
}


class DataService:
    def __init__(self):
        self._player_model = PlayerModel()

    def build_model(self, league: League, field: Field):
        with get_session() as session:
            rows = self._build_model_rows(session, league, field)

        players_in_model = set()
        for row in rows:
            players_in_model.add(row.player_id)

        exists = self._player_model.model_exists(league, field)

        if not exists:
            self._player_model.build_model(league, field, rows)

        return list(players_in_model)

    def make_prediction(
        self,
        match: Match,
        players_in_model: list[Player],
        field: Field,
        over: float,
        odds: list[Odds],
    ):
        player_to_odds = {odds.player: odds for odds in odds}
        players = list(player_to_odds.keys())

        with get_session() as session:
            predict_rows = [
                row
                for row in self._build_predict_rows(session, match)
                if row.player_id in players_in_model
            ]

        predictions = self._player_model.predict_probabilities(
            match.league, field, predict_rows, over
        )

        rows = []
        for row, prediction in zip(predict_rows, predictions):
            player_match = self._find_most_similar_name(row.player_name, players)

            if player_match is None:
                continue

            row = io.Row(
                player=row.player_name,
                team=row.team,
                opponent=row.opponent,
                venue="home" if row.is_home else "away",
                odds=player_to_odds[player_match].value,
                prediction=prediction,
            )

            rows.append(row)

        return rows

    def _build_model_rows(
        self,
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
            .where(Match.league == league)
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

    def _get_current_players(self, session: Session, team_id: str) -> list[Player]:
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

    def _build_predict_rows(
        self, session: Session, match: FbrefMatch
    ) -> list[PredictRow]:
        home_team = get_or_create_team(session, match.home_team)
        home_players = self._get_current_players(session, home_team.id)

        away_team = get_or_create_team(session, match.away_team)
        away_players = self._get_current_players(session, away_team.id)

        rows: list[PredictRow] = []

        for player in home_players:
            avg_minutes = get_avg_minutes_played_when_started(
                session, player.id, match.season
            )
            row = PredictRow(
                player_id=str(player.id),
                player_name=player.name,
                team_id=str(home_team.id),
                team=home_team.name,
                opponent_id=str(away_team.id),
                opponent=away_team.name,
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
                team=away_team.name,
                opponent_id=str(home_team.id),
                opponent=home_team.name,
                is_home=0,
                started=1,
                avg_minutes=int(avg_minutes),
            )
            rows.append(row)

        return rows

    def _get_dispersion_by_league(self, session: Session, league: League, field: Field):
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
            .join(Match, PlayerMatchReport.match_id == Match.id)
            .where(Match.league == league)
            .where(PlayerMatchReport.min >= 60)
        )

        return session.execute(stmt).first()

    def _create_player_match_report(
        self, session: Session, fbref_report: MatchReport, match_id: int, team_id: int
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

    def create_fbref_match(self, session: Session, fbref_match: MatchWithReports):
        home_team = get_or_create_team(session, team_name=fbref_match.home_team)
        away_team = get_or_create_team(session, team_name=fbref_match.away_team)

        match = get_or_create_match(
            session,
            league=fbref_match.league,
            season=fbref_match.season,
            home_team_id=home_team.id,
            away_team_id=away_team.id,
            date=fbref_match.date,
        )

        reports_to_create: list[PlayerMatchReport] = []

        for fbref_report in fbref_match.home_reports:
            report = self._create_player_match_report(
                session, fbref_report, match_id=match.id, team_id=home_team.id
            )
            reports_to_create.append(report)

        for fbref_report in fbref_match.away_reports:
            report = self._create_player_match_report(
                session, fbref_report, match_id=match.id, team_id=away_team.id
            )
            reports_to_create.append(report)

        create_many_reports(session, reports_to_create)

        session.commit()

    @staticmethod
    def _find_most_similar_name(target_name, name_list) -> str | None:
        """
        Finds the closest match to target_name within name_list.
        Returns None if the list is empty.
        """
        # get_close_matches returns a list of matches ranked by similarity
        # n=1 ensures we only get the single best match
        # cutoff=0.0 ensures we get the best match even if it's not very similar
        matches = difflib.get_close_matches(target_name, name_list, n=1, cutoff=0.0)

        return matches[0] if matches else None
