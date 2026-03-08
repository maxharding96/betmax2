from scraper import Scraper
from .helpers import get_matches_ext, get_schedule_ext, str_to_league
from schemas import League, Season
import pandas as pd
import io
from nodriver import Element
from datetime import datetime
from fbref.schema import MatchReport, Match, MatchWithReports


BASE_URL = "https://fbref.com"


class FBRef:
    _base_url: str
    _scraper: Scraper

    def __init__(self, scraper: Scraper):
        self._base_url = BASE_URL
        self._scraper = scraper

    async def get_date_matches(
        self, league: League, season: Season, date: str
    ) -> list[Match]:
        ext = get_matches_ext(date)
        url = self._base_url + ext

        page = await self._scraper.get_page(url)

        all_tables = await page.select_all("table")

        matches: list[Match] = []

        for table in all_tables:
            df = await self._parse_table(table)
            # Check is a table of matches
            if df.columns[0] != "Round":
                continue

            # Check if table is league you want
            df_league = str_to_league.get(df.iat[0, 0])

            if df_league is None or league != df_league:
                continue

            for row in df.itertuples():
                match = Match(
                    league=league,
                    season=season,
                    home_team=row.Home,
                    away_team=row.Away,
                    date=datetime.today(),
                )

                matches.append(match)

            # Found the league table we want
            break

        return matches

    async def get_played_matches(
        self,
        league: League,
        season: Season,
        *,
        start_index: int = 0,
        end_index: int = -1,
    ):
        ext = get_schedule_ext(league, season)
        url = self._base_url + ext

        page = await self._scraper.get_page(url)

        mr_elements = await page.find_all("Match Report")
        mr_exts = [el.attrs.get("href") for el in mr_elements if el.tag_name == "a"]

        for match_ext in mr_exts[start_index:end_index]:
            try:
                match = await self._get_match(league, season, match_ext)
                yield match
            except Exception as e:
                print(f"Failed to scrape {match_ext}: {e}")
                continue

    async def _get_match(
        self, league: League, season: Season, ext: str
    ) -> MatchWithReports:
        url = self._base_url + ext
        page = await self._scraper.get_page(url)

        header_tag = await page.select("h1")
        header = header_tag.text

        home_team, away_team = self._parse_teams(header)
        match_date = self._parse_date(header)

        all_tables = await page.select_all("table")

        home_reports = await self._get_team_match_reports(
            report_table=all_tables[-4], lineup_table=all_tables[-7]
        )

        away_reports = await self._get_team_match_reports(
            report_table=all_tables[-2], lineup_table=all_tables[-6]
        )

        return MatchWithReports(
            league=league,
            season=season,
            home_team=home_team,
            away_team=away_team,
            date=match_date,
            home_reports=home_reports,
            away_reports=away_reports,
        )

    async def _get_team_match_reports(
        self, *, report_table: Element, lineup_table: Element
    ) -> list[MatchReport]:
        report_df = await self._parse_table(report_table, drop_level=True)
        lineup_df = await self._parse_table(lineup_table)

        lineup_dict = self._create_lineup_dict(lineup_df)
        report_df["started"] = report_df["Player"].map(lineup_dict)

        df = report_df.iloc[:-1]

        reports: list[MatchReport] = []

        for row in df.itertuples(index=False):
            # Must not include goalkeepers
            if row.Pos == "GK":
                continue

            report = MatchReport(
                player=row.Player,
                started=row.started,
                min=row.Min,
                sh=row.Sh,
                sot=row.SoT,
                fld=row.Fld,
                fls=row.Fls,
            )

            reports.append(report)

        return reports

    @staticmethod
    async def _parse_table(table: Element, *, drop_level: bool = False) -> pd.DataFrame:
        html = await table.get_html()

        dfs = pd.read_html(io.StringIO(html))
        df = dfs[0]

        if drop_level:
            df.columns = df.columns.droplevel(0)

        return df

    @staticmethod
    def _create_lineup_dict(df: pd.DataFrame) -> dict[str, bool]:
        did_start = True
        lineup_dict = {}

        for _, player in df.itertuples(index=False):
            if player == "Bench":
                did_start = False
            else:
                lineup_dict[player] = did_start

        return lineup_dict

    @staticmethod
    def _parse_teams(header: str) -> tuple[str, str]:
        teams = header.split("Match Report")[0].strip()
        return teams.split(" vs. ")

    @staticmethod
    def _parse_date(header: str) -> datetime:
        date_str = header.split("–")[1].strip()
        return datetime.strptime(date_str, "%A %B %d, %Y")
