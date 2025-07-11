from playwright.sync_api import Page
from utils.read_config import AppConfiguration

class MenuPage:
    def __init__(self, page: Page):
        self.page = page
        config = AppConfiguration.get_app_configuration()
        self.default_navigation_timeout = int(config["DefaultNavigationTimeout"])
        self.default_timeout = int(config["DefaultTimeout"])

    def open_menu(self):
        self.page.click('button[id="react-burger-menu-btn"]', timeout=self.default_timeout)

    def close_menu(self):
        self.page.click('button[id="react-burger-cross-btn"]', timeout=self.default_timeout)

    def logout(self):
        self.page.click('a[id="logout_sidebar_link"]', timeout=self.default_timeout)

    def click_reset_app_state_on_products_page(self):
        self.page.click('//a[@data-test="reset-sidebar-link"]', timeout=self.default_timeout)
        self.page.wait_for_load_state('load', timeout=self.default_navigation_timeout)
        assert 'inventory.html' in self.page.url, "Actual result: Reset app state did not navigate to inventory page\nExpected result: inventory.html should be in the URL"
        assert not self.page.locator('button', has_text='Remove').is_visible(), "Actual result: Remove buttons are still present after reset\nExpected result: Remove buttons should not be visible after reset"

    def click_reset_app_state_on_cart_page(self):
        self.page.click('//a[@data-test="reset-sidebar-link"]', timeout=self.default_timeout)
        self.page.wait_for_load_state('load', timeout=self.default_navigation_timeout)
        assert 'cart.html' in self.page.url, "Actual result: Reset app state did not navigate to cart page\nExpected result: cart.html should be in the URL"
        assert not self.page.locator('.cart_item').is_visible(), "Actual result: Cart items are still present after reset\nExpected result: Cart items should not be visible after reset"

    def click_all_items(self):
        self.page.click('a[id="inventory_sidebar_link"]', timeout=self.default_timeout)
        assert 'inventory.html' in self.page.url, "Actual result: Clicking 'All Items' did not navigate to inventory page\nExpected result: inventory.html should be in the URL"
        self.page.wait_for_load_state('load', timeout=self.default_navigation_timeout)
        assert self.page.locator('.inventory_item').count() > 0, "Actual result: No items found on inventory page after clicking 'All Items'\nExpected result: Items should be present on inventory page"

    def click_about(self):
        self.page.click('//a[@data-test="about-sidebar-link"]', timeout=self.default_timeout)
        self.page.wait_for_load_state('domcontentloaded', timeout=self.default_navigation_timeout)
        assert 'https://saucelabs.com/' in self.page.url, "Actual result: Clicking 'About' did not navigate to Sauce Labs website\nExpected result: Sauce Labs website should be opened"