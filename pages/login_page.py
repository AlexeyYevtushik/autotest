from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def login(self, username: str, password: str):
        self.page.fill('input[data-test="username"]', username)
        self.page.fill('input[data-test="password"]', password)
        self.page.click('input[data-test="login-button"]')

    def get_error(self):
        return self.page.locator('[data-test="error"]')
