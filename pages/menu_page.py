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
        self.page.wait_for_load_state('networkidle', timeout=self.default_navigation_timeout)
        assert 'inventory.html' in self.page.url, "Reset app state did not navigate to inventory page"
        assert not self.page.locator('button', has_text='Remove').is_visible(), "Remove buttons are still present after reset"

    def click_reset_app_state_on_cart_page(self):
        self.page.click('//a[@data-test="reset-sidebar-link"]', timeout=self.default_timeout)
        self.page.wait_for_load_state('networkidle', timeout=self.default_navigation_timeout)
        assert 'cart.html' in self.page.url, "Reset app state did not navigate to cart page"
        assert not self.page.locator('.cart_item').is_visible(), "Cart items are still present after reset"

