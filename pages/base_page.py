from playwright.sync_api import Page, Locator
from utils.read_config import AppConfiguration


class BasePage:
    def __init__(self, page: Page):
        self.current_page = page
        config = AppConfiguration.get_app_configuration()
        self.default_navigation_timeout = int(config["DefaultNavigationTimeout"])
        self.default_timeout = int(config["DefaultTimeout"])

    def screen_title(self) -> Locator:
        title_selector = self.current_page.locator(Selectors.ScreenTitle)
        return title_selector


class Selectors:
    ScreenTitle = ".title"