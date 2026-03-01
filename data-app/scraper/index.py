import nodriver as uc
import asyncio
import random


CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


class Scraper:
    _browser: uc.Browser

    def __init__(self, browser: uc.Browser):
        self._browser = browser

    @classmethod
    async def start(cls):
        config = uc.Config()
        config.browser_executable_path = CHROME_PATH

        browser = await uc.start(config=config)

        return cls(browser)

    def stop(self):
        self._browser.stop()

    async def get_page(self, url: str) -> uc.Tab:
        print(f"Navigating to: {url}")
        page = await self._browser.get(url)

        await self._delay()

        return page

    @staticmethod
    async def _delay():
        wait = 5 + 5 * random.random()
        print(f"Waiting for {wait:.2f}s...")
        await asyncio.sleep(wait)
