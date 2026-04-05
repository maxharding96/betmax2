import nodriver as uc
import asyncio
import random


CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


class Scraper:
    _browser: uc.Browser | None
    _tab: uc.Tab | None

    def __init__(self):
        self._browser = None
        self._tab = None

    async def _get_browser(self) -> uc.Browser:
        if self._browser is None:
            self._browser = await self._start()

        return self._browser

    @staticmethod
    async def _start():
        config = uc.Config()
        config.browser_executable_path = CHROME_PATH
        config.add_argument("--window-size=1440,900")

        browser = await uc.start(config=config)
        return browser

    def stop(self):
        if self._browser:
            self._browser.stop()
            self._browser = None
            self._tab = None

    async def get_page(self, url: str) -> uc.Tab:
        print(f"Navigating to: {url}")

        browser = await self._get_browser()

        if not self._tab:
            self._tab = await browser.get(url)
        else:
            await self._tab.get(url)

        await self._tab.scroll_down(random.randint(100, 300))
        await self._wait()

        return self._tab

    @staticmethod
    async def _wait():
        wait = random.uniform(1.5, 4.0)
        print(f"Waiting for {wait:.2f}s...")
        await asyncio.sleep(wait)
