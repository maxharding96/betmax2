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

    # TODO: how do we want to handle this?
    async def handle_tasks(self):
        pass

    async def _get_page_content(self, url: str) -> str:
        print(f"Navigating to: {url}")
        page = await self._browser.get(url)

        await self._human_delay(mu=3, sigma=0.8)

        return page.get_content()

    @staticmethod
    async def _human_delay(mu=4.0, sigma=1.5):
        """
        Uses a Gaussian (normal) distribution for sleep times.
        mu: average sleep time.
        sigma: how much the 'mood' varies.
        """
        wait = max(1.8, random.gauss(mu, sigma))
        print(f"Waiting for {wait:.2f}s...")
        await asyncio.sleep(wait)
