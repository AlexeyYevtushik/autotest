from playwright.sync_api import Page
from utils.read_config import AppConfiguration

class CartPage:
    def __init__(self, page: Page):
        self.page = page
        config = AppConfiguration.get_app_configuration()
        self.default_navigation_timeout = int(config["DefaultNavigationTimeout"])
        self.default_timeout = int(config["DefaultTimeout"])

    def checkout(self):
        self.page.click('button[data-test="checkout"]', timeout=self.default_timeout)

    def remove_item(self, item_test_id: str):
        self.page.click(f'button[data-test="remove-{item_test_id}"]', timeout=self.default_timeout)

    def is_cart_empty(self):
        return self.page.locator('.cart_item').count() == 0
    
    def click_continue_shopping(self):
        self.page.click('button[data-test="continue-shopping"]', timeout=self.default_timeout)
        assert 'inventory.html' in self.page.url

    def assert_cart_is_empty(self):
        assert self.is_cart_empty(), "Cart is not empty, items are still present."
