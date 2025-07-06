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
