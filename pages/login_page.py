from playwright.sync_api import Page
from utils.read_config import AppConfiguration
from pages.base_page import BasePage

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        config = AppConfiguration.get_app_configuration()
        self.default_navigation_timeout = int(config["DefaultNavigationTimeout"])
        self.default_timeout = int(config["DefaultTimeout"])

    def login(self, username="standard_user", password="secret_sauce"):
        self.page.fill('input[data-test="username"]', username, timeout=self.default_timeout)
        self.page.fill('input[data-test="password"]', password, timeout=self.default_timeout)
        self.page.click('input[data-test="login-button"]', timeout=self.default_timeout)

    def get_error(self):
        return self.page.locator('[data-test="error"]')

    def expect_logged_out(self):
        assert self.page.locator('input[data-test="username"]').is_visible(), "Actual result: Username field is not visible, user might still be logged in\nExpected result: Username field is visible"
        assert self.page.locator('input[data-test="password"]').is_visible(), "Actual result: Password field is not visible, user might still be logged in\nExpected result: Password field is visible"

    def expect_login_error(self, message):
        error_locator = self.page.locator('[data-test="error"]')
        assert error_locator.is_visible(), "Actual result: Error message is not visible\nExpected result: Error message should be visible"
        assert error_locator.inner_text() == message, f"Actual result: Expected error message '{message}', but got '{error_locator.inner_text()}'\nExpected result: Error message should match"

    def check_page_image(self, page_name: str = "login",  threshold: int = 10) -> bool:
        base_page = BasePage(self.page)
        base_page.check_page_image(f"tests/tmp/current_{page_name}_page.png", f"tests/tmp/{page_name}_page_expected.png", threshold)