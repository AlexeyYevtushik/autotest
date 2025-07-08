from playwright.sync_api import Page
from utils.read_config import AppConfiguration

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
        assert error_locator.is_visible(), "Error message is not visible"
        return error_locator.inner_text()
