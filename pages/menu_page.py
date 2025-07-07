from playwright.sync_api import Page

class MenuPage:
    def __init__(self, page: Page):
        self.page = page

    def open_menu(self):
        self.page.click('button[id="react-burger-menu-btn"]')

    def close_menu(self):
        self.page.click('button[id="react-burger-cross-btn"]')      

    def logout(self):
        self.page.click('a[id="logout_sidebar_link"]')

    def click_reset_app_state_on_products_page(self):
        self.page.click('//a[@data-test="reset-sidebar-link"]')
        self.page.wait_for_load_state('networkidle')
        assert 'inventory.html' in self.page.url, "Reset app state did not navigate to inventory page"
        assert not self.page.locator('button', has_text='Remove').is_visible(), "Remove buttons are still present after reset"

    def click_reset_app_state_on_cart_page(self):
        self.page.click('//a[@data-test="reset-sidebar-link"]')
        self.page.wait_for_load_state('networkidle')
        assert 'cart.html' in self.page.url, "Reset app state did not navigate to cart page"
        assert not self.page.locator('.cart_item').is_visible(), "Cart items are still present after reset"

