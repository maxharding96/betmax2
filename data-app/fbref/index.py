from scraper import Scraper
from .helpers import get_schedule_ext
from schemas import League, Season
import pandas as pd
import io
from nodriver import Element
from datetime import datetime
from fbref.schema import MatchReport, Match


BASE_URL = "https://fbref.com"


class FBRef:
    _base_url: str
    _scraper: Scraper

    def __init__(self, scraper: Scraper):
        self._base_url = BASE_URL
        self._scraper = scraper

    async def get_matches(
        self, league: League, season: Season, *, start_index: int = 0
    ):
        ext = get_schedule_ext(league, season)
        url = self._base_url + ext

        page = await self._scraper.get_page(url)

        mr_elements = await page.find_all("Match Report")
        mr_exts = [el.attrs.get("href") for el in mr_elements if el.tag_name == "a"]

        for match_ext in mr_exts[start_index:]:
            try:
                match = await self._get_match(league, season, match_ext)
                yield match
            except Exception as e:
                print(f"Failed to scrape {match_ext}: {e}")
                continue

    async def _get_match(self, league: League, season: Season, ext: str) -> Match:
        url = self._base_url + ext
        page = await self._scraper.get_page(url)

        header_tag = await page.select("h1")
        header = header_tag.text

        home_team, away_team = self._parse_teams(header)
        date = self._parse_date(header)

        all_tables = await page.select_all("table")

        home_reports = await self._get_team_match_reports(
            report_table=all_tables[-4], lineup_table=all_tables[-7]
        )

        away_reports = await self._get_team_match_reports(
            report_table=all_tables[-2], lineup_table=all_tables[-6]
        )

        return Match(
            league=league,
            season=season,
            home_team=home_team,
            away_team=away_team,
            date=date,
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
