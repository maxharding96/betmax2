from scraper import Scraper
from .helpers import get_schedule_ext
from schemas import League, Season
import pandas as pd
import io
from nodriver import Element

BASE_URL = "https://fbref.com"


class FBRef:
    _base_url: str
    _scraper: Scraper

    def __init__(self, scraper: Scraper):
        self._base_url = BASE_URL
        self._scraper = scraper

    async def get_match_reports(self, league: League, season: Season):
        ext = get_schedule_ext(league, season)
        url = self._base_url + ext

        page = await self._scraper.get_page(url)

        mr_elements = await page.find_all("Match Report")
        mr_exts = [el.attrs.get("href") for el in mr_elements if el.tag_name == "a"]

        for match_ext in mr_exts:
            try:
                df = await self._get_match_report(match_ext)
                yield df
            except Exception as e:
                print(f"Failed to scrape {match_ext}: {e}")
                continue

    async def _get_match_report(self, ext: str) -> pd.DataFrame:
        url = self._base_url + ext
        page = await self._scraper.get_page(url)

        all_tables = await page.select_all("table")

        home_table = all_tables[-4]
        away_table = all_tables[-2]

        home_df = await self._parse_table(home_table, drop_level=True)
        away_df = await self._parse_table(away_table, drop_level=True)

        return pd.concat([home_df, away_df], axis=0)

    @staticmethod
    async def _parse_table(table: Element, *, drop_level: bool = False) -> pd.DataFrame:
        html = await table.get_html()

        dfs = pd.read_html(io.StringIO(html))
        df = dfs[0]

        if drop_level:
            df.columns = df.columns.droplevel(0)

        return df
