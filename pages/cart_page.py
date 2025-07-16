from playwright.sync_api import Page
from pages import base_page
from utils.read_config import AppConfiguration
from pages.base_page import BasePage

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
        assert self.is_cart_empty(), "Actual result: Cart is not empty, items are still present.\nExpected result: Cart should be empty."

    def check_page_image(self, page_name: str = "cart", threshold: int = 10) -> bool:
        base_page = BasePage(self.page)
        base_page.check_page_image(f"tests/tmp/current_{page_name}_page.png", f"tests/tmp/{page_name}_page_expected.png", threshold)