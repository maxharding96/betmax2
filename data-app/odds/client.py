from scraper import Scraper
from schemas import Field
from .helpers import get_odds_ext, field_to_str
from .schema import MatchOdds, FieldOdds, Odds
from nodriver import Tab
from fbref.schema import Match

BASE_URL = "https://www.oddschecker.com/football"


class OddsChecker:
    _base_url: str
    _scraper: Scraper

    def __init__(self, scraper: Scraper):
        self._base_url = BASE_URL
        self._scraper = scraper

    async def get_odds(self, match: Match, fields: list[Field]) -> MatchOdds | None:
        url = self._base_url + get_odds_ext(match)

        page = await self._scraper.get_page(url)

        player_betting_btn = await page.find(
            "#market_filters_Player-Betting_Player-Betting"
        )
        if not player_betting_btn:
            return None

        await player_betting_btn.click()

        fields_odds = []

        for field in fields:
            field_odds = await self.get_field_odds(page, field)
            if field_odds:
                fields_odds.append(field_odds)

        return MatchOdds(match=match, fields_odds=fields_odds)

    async def get_field_odds(self, page: Tab, field: Field) -> FieldOdds | None:
        headers = await page.find_all("h2")
        header = next((h for h in headers if h.text == field_to_str[field]), None)
        if not header:
            return None

        await header.click()
        await page.sleep(2)

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

        return FieldOdds(field=field, odds=odds)
