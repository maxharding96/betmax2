from scraper import Scraper
from schemas import Field, League, Season
from .helpers import (
    get_odds_ext,
    field_to_str,
    league_to_ext,
    league_to_team_selector,
    convert_to_fbref_team,
)
from .schema import MatchOdds, Odds
from nodriver import Tab
from fbref.schema import Match
from datetime import datetime

BASE_URL = "https://www.oddschecker.com/football"


class OddsChecker:
    _base_url: str
    _scraper: Scraper

    def __init__(self, scraper: Scraper):
        self._base_url = BASE_URL
        self._scraper = scraper

    async def get_matches(self, league: League) -> list[Match]:
        url = self._base_url + league_to_ext[league]

        page = await self._scraper.get_page(url)

        see_all_matches_btn = await page.find("a[class*='AllMatchesLink']")

        if see_all_matches_btn:
            await see_all_matches_btn.click()
            await page.sleep(0.2)

        team_selector = league_to_team_selector[league]

        teams = await page.find_all(team_selector)

        matches: list[Match] = []

        for i in range(0, len(teams), 2):
            home_team = convert_to_fbref_team(teams[i].text)
            away_team = convert_to_fbref_team(teams[i + 1].text)

            match = Match(
                home_team=home_team,
                away_team=away_team,
                league=league,
                season=Season.S_25,
                date=datetime.now(),
            )
            matches.append(match)

        return matches

    async def get_odds(self, match: Match, fields: list[Field]) -> MatchOdds | None:
        url = self._base_url + get_odds_ext(match)

        page = await self._scraper.get_page(url)

        player_betting_btn = await page.find(
            "#market_filters_Player-Betting_Player-Betting"
        )
        if not player_betting_btn:
            return None

        await player_betting_btn.click()

        field_to_odds = {}

        for field in fields:
            field_odds = await self.get_field_odds(page, field)
            if field_odds:
                field_to_odds[field] = field_odds

        return MatchOdds(match=match, field_to_odds=field_to_odds)

    async def get_field_odds(self, page: Tab, field: Field) -> list[Odds] | None:
        headers = await page.find_all("h2")
        header = next((h for h in headers if h.text == field_to_str[field]), None)
        if not header:
            return None

        await header.click()
        await page.sleep(0.2)

        parent_div = header.parent
        if not parent_div:
            return

        show_more_span = await parent_div.query_selector('span[class*="ShowMoreText"]')
        if show_more_span:
            await show_more_span.click()

        odds = []

        player_paragraphs = await parent_div.query_selector_all(
            'p[class*="MarketExpanderBet"]'
        )
        odds_buttons = await parent_div.query_selector_all("button")

        for pp, ob in zip(player_paragraphs, odds_buttons):
            bet_name = pp.text
            value = ob.text

            if not bet_name or not value:
                continue

            parts = bet_name.split(" ")
            point = parts.pop()

            if not point:
                continue

            odds.append(
                Odds(
                    point=float(point),
                    player=" ".join(parts),
                    value=value,
                )
            )

        return odds
