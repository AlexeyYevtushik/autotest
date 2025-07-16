from playwright.sync_api import Page
from utils.read_config import AppConfiguration
from pages.base_page import BasePage

class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        config = AppConfiguration.get_app_configuration()
        self.default_navigation_timeout = int(config["DefaultNavigationTimeout"])
        self.default_timeout = int(config["DefaultTimeout"])

    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str):
        self.page.fill('input[data-test="firstName"]', first_name, timeout=self.default_timeout)
        self.page.fill('input[data-test="lastName"]', last_name, timeout=self.default_timeout)
        self.page.fill('input[data-test="postalCode"]', postal_code, timeout=self.default_timeout)
        self.page.click('input[data-test="continue"]', timeout=self.default_timeout)

    def finish(self):
        self.page.click('button[data-test="finish"]', timeout=self.default_timeout)

    def get_confirmation(self):
        return self.page.locator('.complete-header')

    def click_back_to_products(self):
        self.page.click('button[data-test="back-to-products"]', timeout=self.default_timeout)

    def click_cancel(self):
        self.page.click('button[data-test="cancel"]', timeout=self.default_timeout)

    def assert_error_is_visible(self):
        error_locator = self.page.locator('*[data-test="error"]')
        assert error_locator.is_visible(), "Actual result: Error message is not visible\nExpected result: Error message should be visible"
        return error_locator.inner_text(), "Actual result: Error message text does not match expected\nExpected result: Error message should be visible"
    
    def expect_confirmation_to_have_text(self, text: str):
        """Assert that the confirmation message contains the specified text."""
        confirmation_locator = self.get_confirmation()
        assert confirmation_locator.is_visible(), "Actual result: Confirmation message is not visible\nExpected result: Confirmation message should be visible"
        confirmation_text = confirmation_locator.inner_text()
        assert text in confirmation_text, f"Actual result: Expected confirmation to contain '{text}', but got '{confirmation_text}'\nExpected result: Confirmation message should match"

    def check_page_image(self, page_name: str = "checkout", threshold: int = 10) -> bool:
        base_page = BasePage(self.page)
        base_page.check_page_image(f"tests/tmp/current_{page_name}_page.png", f"tests/tmp/{page_name}_page_expected.png", threshold)