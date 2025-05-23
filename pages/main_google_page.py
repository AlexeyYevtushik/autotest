from playwright.sync_api import Page
from utils.logger import logger
from pages.base_page import BasePage


class MainGooglePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self._selectors = self._Selectors()
        logger.info("MainGooglePage initialized.")

    def click_accept_all_cookies(self):
        accept_all_cookies = self.page.locator(self._selectors.ACCEPT_ALL_COOKIES)
        accept_all_cookies.click()
        logger.info("Clicked 'Accept All' button")

    class _Selectors:
        ACCEPT_ALL_COOKIES = "//button/*[contains(text(), 'Accept all')]"
