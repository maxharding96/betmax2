from scraper import Scraper

BASE_URL = "https://fbref.com/en"


class FBRef:
    _base_url: str
    _scraper: Scraper

    def __init__(self, scraper: Scraper):
        self._base_url = BASE_URL
        self._scraper = scraper
