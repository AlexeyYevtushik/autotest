from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from utils.logger import logger
from pages.base_page import BasePage


class MainGooglePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self._selectors = self._Selectors()
        logger.info("MainGooglePage initialized.")

    def click_accept_all_cookies(self):
        try:
            # Try multiple possible selectors for the cookie consent button
            for selector in [
                self._selectors.ACCEPT_ALL_COOKIES,
                self._selectors.ACCEPT_ALL_COOKIES_ALT1,
                self._selectors.ACCEPT_ALL_COOKIES_ALT2,
                self._selectors.ACCEPT_ALL_COOKIES_ALT3
            ]:
                try:
                    button = self.page.locator(selector)
                    # Wait for button to be visible and stable
                    button.wait_for(state="visible", timeout=5000)
                    if button.is_visible():
                        button.click()
                        logger.info(f"Clicked 'Accept All' button using selector: {selector}")
                        return
                except PlaywrightTimeoutError:
                    continue
            
            logger.warning("No cookie consent button found")
        except Exception as e:
            logger.error(f"Error handling cookie consent: {str(e)}")

    class _Selectors:
        ACCEPT_ALL_COOKIES = "//button/*[contains(text(), 'Accept all')]"
        ACCEPT_ALL_COOKIES_ALT1 = "button[id*='consent']"
        ACCEPT_ALL_COOKIES_ALT2 = "[aria-label*='Accept']"
        ACCEPT_ALL_COOKIES_ALT3 = "form[action*='consent'] button"
